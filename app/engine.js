/*
 * The valuation engine in JavaScript: a line-for-line port of src/valuation.py,
 * so the browser can run the DCF and the Monte Carlo live.
 * Parity with Python is checked by app/engine.test.js (run: node app/engine.test.js).
 */
(function (root) {
  "use strict";

  // ---------- one forecast year (same formulas as valuation._year) ----------
  function year(i, t, revenuePrev, g1, marginTarget, gTerm) {
    const terminal = t === i.years + 1;
    const growth = terminal ? gTerm : g1 + (gTerm - g1) * (t - 1) / i.years;
    const step = Math.min(t, i.years) / i.years;
    const margin = i.margin0 + (marginTarget - i.margin0) * step;
    const daPct = i.da_pct0 + (i.capex_pct - i.da_pct0) * step;
    const revenue = revenuePrev * (1 + growth);
    const ebitda = revenue * margin;
    const da = revenue * daPct;
    const ebit = ebitda - da;
    const tax = ebit * i.tax_rate;
    const capex = revenue * i.capex_pct;
    const dNwc = i.nwc_pct * (revenue - revenuePrev);
    const fcff = ebit - tax + da - capex - dNwc;
    return { growth, revenue, ebitda_margin: margin, ebitda, da, ebit, tax, capex, change_nwc: dNwc, fcff };
  }

  // ---------- the forecast table ----------
  function project(i) {
    const rows = [];
    let prev = i.revenue0;
    for (let t = 1; t <= i.years + 1; t++) {
      const y = year(i, t, prev, i.g1, i.margin_target, i.g_term);
      y.year = t;
      y.discount_factor = t === i.years + 1 ? null : 1 / Math.pow(1 + i.wacc, t);
      y.pv_fcff = y.discount_factor === null ? null : y.fcff * y.discount_factor;
      rows.push(y);
      prev = y.revenue;
    }
    return rows;
  }

  // ---------- the DCF ----------
  function dcf(i) {
    const p = project(i);
    const explicit = p.slice(0, i.years);
    const last = p[i.years];
    const pvExplicit = explicit.reduce((s, r) => s + r.pv_fcff, 0);
    const terminalValue = last.fcff / (i.wacc - i.g_term);
    const pvTerminal = terminalValue / Math.pow(1 + i.wacc, i.years);
    const ev = pvExplicit + pvTerminal;
    const equity = ev - i.debt + i.cash;
    return {
      pv_explicit: pvExplicit, terminal_value: terminalValue, pv_terminal: pvTerminal,
      terminal_share_of_ev: pvTerminal / ev, enterprise_value: ev, equity_value: equity,
      value_per_share: equity / i.shares, implied_terminal_ev_ebitda: terminalValue / last.ebitda,
      table: p,
    };
  }

  // Fast path for the Monte Carlo: value per share only
  function valuePerShare(i, g1, marginTarget, wacc, gTerm) {
    let prev = i.revenue0, pv = 0;
    for (let t = 1; t <= i.years + 1; t++) {
      const y = year(i, t, prev, g1, marginTarget, gTerm);
      pv += t === i.years + 1 ? y.fcff / (wacc - gTerm) / Math.pow(1 + wacc, i.years)
                               : y.fcff / Math.pow(1 + wacc, t);
      prev = y.revenue;
    }
    return (pv - i.debt + i.cash) / i.shares;
  }

  // ---------- reverse DCF: the year-1 growth that makes value = price (bisection) ----------
  function impliedGrowth(i, price, lo = -0.3, hi = 0.8) {
    const f = (g) => valuePerShare(i, g, i.margin_target, i.wacc, i.g_term) - price;
    if (f(lo) > 0 || f(hi) < 0) return null;
    for (let k = 0; k < 100; k++) {
      const mid = (lo + hi) / 2;
      if (f(mid) > 0) hi = mid; else lo = mid;
      if (hi - lo < 1e-7) break;
    }
    return (lo + hi) / 2;
  }

  // ---------- random numbers ----------
  // mulberry32: small, fast, seedable, so a run can be repeated exactly
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Triangular distribution (low, most likely, high) by inverse transform
  function triangular(u, low, mode, high) {
    if (high <= low) return mode;
    const c = (mode - low) / (high - low);
    return u < c ? low + Math.sqrt(u * (high - low) * (mode - low))
                 : high - Math.sqrt((1 - u) * (high - low) * (high - mode));
  }

  // ---------- Monte Carlo ----------
  // spec: { g1:[lo,mode,hi], margin:[lo,mode,hi], wacc:[lo,mode,hi], gTerm:[lo,hi] }
  function monteCarlo(i, spec, n, seed) {
    const r = rng(seed);
    const g1 = new Float64Array(n), mg = new Float64Array(n), w = new Float64Array(n),
          gt = new Float64Array(n), v = new Float64Array(n);
    for (let k = 0; k < n; k++) {
      g1[k] = triangular(r(), spec.g1[0], spec.g1[1], spec.g1[2]);
      mg[k] = triangular(r(), spec.margin[0], spec.margin[1], spec.margin[2]);
      w[k] = triangular(r(), spec.wacc[0], spec.wacc[1], spec.wacc[2]);
      gt[k] = spec.gTerm[0] + r() * (spec.gTerm[1] - spec.gTerm[0]);
      // guard: the Gordon formula needs WACC above terminal growth
      v[k] = w[k] - gt[k] > 0.005 ? valuePerShare(i, g1[k], mg[k], w[k], gt[k]) : NaN;
    }
    return { g1, margin: mg, wacc: w, gTerm: gt, value: v, n };
  }

  // ---------- statistics ----------
  function quantile(sorted, q) {
    if (!sorted.length) return NaN;
    const pos = (sorted.length - 1) * q, lo = Math.floor(pos), hi = Math.ceil(pos);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
  }

  function correlation(x, y) {
    let n = 0, sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
    for (let k = 0; k < x.length; k++) {
      if (!isFinite(y[k])) continue;
      n++; sx += x[k]; sy += y[k]; sxx += x[k] * x[k]; syy += y[k] * y[k]; sxy += x[k] * y[k];
    }
    const cov = sxy / n - (sx / n) * (sy / n);
    const vx = sxx / n - (sx / n) ** 2, vy = syy / n - (sy / n) ** 2;
    return vx > 0 && vy > 0 ? cov / Math.sqrt(vx * vy) : 0;
  }

  function decision(median, pAbove, price, rule) {
    if (median >= price * (1 + rule.buy_upside) && pAbove >= rule.buy_probability) return "BUY";
    if (median <= price * (1 - rule.sell_downside)) return "SELL";
    return "HOLD";
  }

  const api = { year, project, dcf, valuePerShare, impliedGrowth, rng, triangular, monteCarlo,
                quantile, correlation, decision };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.Engine = api;
})(typeof window !== "undefined" ? window : globalThis);
