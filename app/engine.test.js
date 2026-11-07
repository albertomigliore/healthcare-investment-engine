/*
 * Parity test: the JavaScript engine must reproduce the Python valuation.
 * Run:  node app/engine.test.js
 */
const fs = require("fs");
const path = require("path");
const E = require("./engine.js");

global.window = {};
eval(fs.readFileSync(path.join(__dirname, "data.js"), "utf8"));
const D = window.APP_DATA;

let failures = 0;
function check(label, got, want, tol) {
  const ok = Math.abs(got - want) <= tol * Math.max(1, Math.abs(want));
  if (!ok) failures++;
  console.log(`${ok ? "ok  " : "FAIL"} ${label}: js ${got.toFixed(4)} vs python ${want.toFixed(4)}`);
}

for (const t of D.finalists) {
  const v = D.valuations[t];
  const i = v.inputs;
  const sc = D.scenarios;
  const shock = (name) => Object.assign({}, i, {
    g1: i.g1 + sc[name].g1, margin_target: i.margin_target + sc[name].margin,
    wacc: i.wacc + sc[name].wacc, g_term: sc[name].g_term,
  });
  // Deterministic DCFs must match to the cent
  check(`${t} DCF base`, E.dcf(i).value_per_share, v.python.dcf_base, 1e-6);
  check(`${t} DCF bear`, E.dcf(shock("bear")).value_per_share, v.python.dcf_bear, 1e-6);
  check(`${t} DCF bull`, E.dcf(shock("bull")).value_per_share, v.python.dcf_bull, 1e-6);
  check(`${t} fast path = table`, E.valuePerShare(i, i.g1, i.margin_target, i.wacc, i.g_term),
        E.dcf(i).value_per_share, 1e-9);
  check(`${t} reverse DCF`, E.impliedGrowth(i, v.price), v.python.implied_year1_growth, 1e-4);

  // Monte Carlo uses a different random generator than numpy, so compare statistically
  const bear = shock("bear"), bull = shock("bull");
  const mc = E.monteCarlo(i, {
    g1: [bear.g1, i.g1, bull.g1], margin: [bear.margin_target, i.margin_target, bull.margin_target],
    wacc: [bull.wacc, i.wacc, bear.wacc], gTerm: [bear.g_term, bull.g_term],
  }, 10000, 42);
  const sorted = Array.from(mc.value).filter(isFinite).sort((a, b) => a - b);
  check(`${t} MC median`, E.quantile(sorted, 0.5), v.python.mc_median, 0.01);
  check(`${t} MC 10th pct`, E.quantile(sorted, 0.1), v.python.mc_p10, 0.015);
  check(`${t} MC 90th pct`, E.quantile(sorted, 0.9), v.python.mc_p90, 0.015);
  const pAbove = sorted.filter((x) => x > v.price).length / sorted.length;
  check(`${t} P(value > price)`, pAbove, v.python.p_value_above_price, 0.03);
}

// Triangular sampler: mean of a triangle is (a + b + c) / 3
const r = E.rng(1);
let s = 0; const n = 200000;
for (let k = 0; k < n; k++) s += E.triangular(r(), 1, 2, 6);
check("triangular mean", s / n, 3, 0.005);

console.log(failures ? `\n${failures} FAILED` : "\nAll parity checks passed");
process.exit(failures ? 1 : 0);
