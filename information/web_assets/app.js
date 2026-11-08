"use strict";
const $ = (id) => document.getElementById(id);
const state = {csv: "", reference: "", title: "", description: "", result: null, view: "relationships", selected: null, busy: false, kind: "weather", source: null, timeline: []};
const colors = ["#a83d25", "#446a7c", "#899271", "#b79554", "#727c89", "#966f7d", "#6f817d", "#b18060", "#888058", "#656d84"];
const controlled = ["weather-load", "city", "stocks-demo", "sensor-demo", "current-file", "reference-file", "target", "bins", "analyze", "remove-reference", "relationships-tab", "drift-tab"];
const bits = (n) => Number(n).toFixed(3);
const pct = n => (n * 100).toFixed(1) + "%";
const friendly = name => ({thermal_state: "Temperature", alarm: "Alarm", zone: "Location", batch: "Batch", fault: "Device health", MSFT: "Microsoft", AMZN: "Amazon", IBM: "IBM", CAT: "Caterpillar", DE: "Deere", F: "Ford"}[name] || name);

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
async function request(url, payload) {
  const response = await fetch(url, payload === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "The analysis could not be completed.");
  return data;
}
function busy(value, message = "") {
  state.busy = value;
  controlled.forEach(id => $(id).disabled = value);
  document.querySelector(".results").setAttribute("aria-busy", String(value));
  $("analyze").textContent = value ? "Working…" : "Explain this data ↗";
  $("weather-load").textContent = value ? "Working…" : "Get recent weather ↗";
  $("status").textContent = message;
  $("status").classList.remove("dirty");
  $("download-report").disabled = value || !state.result;
  $("shuffle-clue").disabled = value || !state.result || state.view !== "relationships" || !state.selected;
  document.querySelectorAll("#bars button").forEach(button => {button.disabled = value;});
}
function error(message) {
  $("error").textContent = message;
  $("error").hidden = !message;
}
function setColumns(columns, preferred) {
  $("target").replaceChildren(...columns.map(name => {
    const option = element("option", friendly(name));
    option.value = name;
    return option;
  }));
  if (columns.includes(preferred)) $("target").value = preferred;
}
function updateReference(name) {
  $("reference-name").textContent = name;
  $("remove-reference").hidden = !state.reference;
}
function invalidate(message = "Ready to explain the current selection.") {
  state.result = null;
  state.selected = null;
  $("download-report").disabled = true;
  $("status").textContent = message;
  $("status").classList.add("dirty");
  $("bars").replaceChildren();
  $("entropy-value").textContent = "—";
  $("reading-title").textContent = "Ready to explore.";
  $("reading-body").textContent = "Choose your target column, then analyze the observations.";
  $("reading-note").textContent = "The results will be calculated from your current selection.";
  $("distribution").replaceChildren();
  $("distribution").setAttribute("aria-label", "No current analysis");
  $("distribution-title").textContent = "Target composition";
  $("distribution-note").textContent = "";
  $("distribution-legend").replaceChildren();
  $("notes").replaceChildren();
  $("takeaway-title").textContent = "Let’s look for a pattern.";
  $("takeaway-body").textContent = "The explanation will appear here when the analysis is ready.";
  $("takeaway-limit").textContent = "This describes patterns in the sample, not what will happen next.";
  $("empty-results").hidden = true;
  $("weather-history").hidden = true;
  $("source-note").hidden = true;
  $("shuffle-result").hidden = true;
  $("shuffle-clue").disabled = true;
  error("");
}
function renderPreview(info) {
  $("preview-summary").textContent = `${info.rows.toLocaleString()} rows · showing ${info.sample.length}`;
  const header = element("tr");
    info.columns.forEach(name => header.append(element("th", friendly(name))));
  $("table-head").replaceChildren(header);
  $("table-body").replaceChildren(...info.sample.map(row => {
    const tr = element("tr");
    info.columns.forEach(name => tr.append(element("td", row[name] === null ? "(missing)" : String(row[name]))));
    return tr;
  }));
}
function renderDistribution() {
  const result = state.result;
  const distribution = result.target_distribution;
  $("distribution-title").textContent = `${friendly(result.report.target)} · what happened`;
  const total = distribution.reduce((sum, row) => sum + row.fraction, 0);
  $("distribution-note").textContent = result.distribution_binned ? "Binned numeric values" : (total < 0.9999 ? "10 most frequent states" : "Observed states");
  const segments = [], labels = [];
  distribution.forEach((row, index) => {
    const label = `${row.state}: ${(row.fraction * 100).toFixed(1)}%`;
    const segment = element("div");
    segment.style.width = `${row.fraction * 100}%`;
    segment.style.backgroundColor = colors[index % colors.length];
    segment.title = `${label} (${row.count} observations)`;
    segments.push(segment);
    const item = element("span");
    const mark = element("i");
    mark.style.backgroundColor = colors[index % colors.length];
    mark.setAttribute("aria-hidden", "true");
    item.append(mark, document.createTextNode(label));
    labels.push(item);
  });
  if (total < 0.9999) {
    const remainder = element("div");
    remainder.style.width = `${(1 - total) * 100}%`;
    remainder.style.backgroundColor = "#d7d8cd";
    segments.push(remainder);
    labels.push(element("span", `Other: ${((1-total)*100).toFixed(1)}%`));
  }
  $("distribution").replaceChildren(...segments);
  $("distribution-legend").replaceChildren(...labels);
  $("distribution").setAttribute("aria-label", `${friendly(result.report.target)}: ${labels.map(n => n.textContent).join("; ")}`);
}
function renderReading(row) {
  const report = state.result.report;
  if (state.view === "relationships") {
    $("reading-title").textContent = friendly(row.feature);
    const example = state.result.explanation.examples[row.feature];
    const info = state.result.explanation;
    if (report.target_entropy_bits === 0) {
      $("reading-body").textContent = `${friendly(report.target)} never changes in this sample, so there is no variation for this clue to help explain.`;
    } else if (row.mutual_information_bits < 1e-10) {
      $("reading-body").textContent = `${friendly(row.feature)} gives no information about ${friendly(report.target)} in this sample. Knowing it doesn’t narrow down the outcome.`;
    } else {
      $("reading-body").textContent = example
        ? countStory(row.feature, example, info)
        : `Knowing ${friendly(row.feature)} removes ${pct(row.fraction_of_target_information)} of the uncertainty about ${friendly(report.target)} in this sample. There aren’t enough repeated states for a useful count example.`;
    }
    $("reading-note").textContent = "The example highlights a condition with a large rate difference. The bar considers all conditions together. Neither proves cause or future accuracy.";
  } else {
    $("reading-title").textContent = friendly(row.column);
    $("reading-body").textContent = row.kl_bits === null
      ? "Something appears in the recent sample that never appeared in the earlier one. The change score is unbounded (∞), so it has no finite bar."
      : row.kl_bits < 1e-10
        ? "The mix of conditions is the same in both samples. This doesn’t mean every relationship stayed the same."
        : `The mix of states for ${friendly(row.column)} changed between the two periods. A larger bar means a bigger change in how often its states appeared.`;
    if (row.column === report.target && !state.result.distribution_binned && state.result.reference_distribution.length) {
      const event = state.result.explanation.event;
      const previous = state.result.reference_distribution.find(item => item.state === event);
      if (previous) $("reading-body").textContent += ` “${event}” went from ${pct(previous.fraction)} earlier to ${pct(state.result.explanation.rate)} now.`;
    }
    $("reading-note").textContent = `Change score: ${row.kl_bits === null ? "∞" : bits(row.kl_bits)} bits (KL divergence). This measures a difference, not whether it is good or bad.`;
  }
}
function renderChart() {
  if (!state.result) return;
  const report = state.result.report;
  const drift = state.view === "drift";
  const rows = drift ? report.drift : report.features;
  const nameOf = row => drift ? row.column : row.feature;
  const valueOf = row => drift ? row.kl_bits : row.fraction_of_target_information * 100;
  const limit = drift ? Math.max(0.1, ...rows.map(row => row.kl_bits || 0)) : 100;
  $("chart-title").textContent = drift ? "What changed from the earlier period?" : `Which clues tell us most about ${state.kind === "stocks" ? friendly(report.target) + "’s daily movement" : friendly(report.target).toLowerCase()}?`;
  $("chart-subtitle").textContent = drift ? "Bigger bars = a bigger change in the mix of conditions." : "Click any clue for an example from the actual data.";
  $("row-label").textContent = drift ? "COLUMN" : "CLUE";
  $("value-label").textContent = drift ? "CHANGE / BITS" : "UNCERTAINTY REMOVED";
  $("axis-mid").textContent = drift ? (limit / 2).toFixed(2) : "50%";
  $("axis-max").textContent = drift ? `${limit.toFixed(2)} bits` : "100%";
  $("chart-explainer").textContent = drift ? "We compare how often each condition appeared in the recent and earlier samples. Seasonal differences can cause changes; this does not diagnose a problem." : "Longer bars mean more information about the outcome in this sample. The percentage measures reduced uncertainty, not prediction accuracy.";
  if (!rows.some(row => nameOf(row) === state.selected)) state.selected = rows.length ? nameOf(rows[0]) : null;
  $("experiment").hidden = drift || !rows.length;
  $("shuffle-result").hidden = true;
  $("shuffle-clue").textContent = `Mix up ${state.selected ? friendly(state.selected) : "this clue"} ↗`;
  $("shuffle-clue").disabled = state.busy || !state.selected;
  $("empty-results").hidden = rows.length !== 0;
  if (!rows.length) {
    $("empty-results").textContent = drift ? "Add a reference CSV, then analyze again to compare distributions." : "This dataset only has the target column. Add another column to explore a relationship.";
    $("reading-title").textContent = drift ? "A point of comparison." : "One more signal.";
    $("reading-body").textContent = drift ? "Use an earlier sample with the same column names. The two samples may have different numbers of rows." : "Each additional column gives the audit something to compare with your outcome.";
    $("reading-note").textContent = "Your existing observations stay available in the preview below.";
  }
  $("bars").replaceChildren(...rows.map(row => {
    const name = nameOf(row), value = valueOf(row);
    const button = element("button", undefined, "bar-row" + (name === state.selected ? " selected" : ""));
    button.dataset.drift = String(drift);
    button.disabled = state.busy;
    button.setAttribute("aria-pressed", String(name === state.selected));
    button.setAttribute("aria-label", `${friendly(name)}, ${value === null ? "unseen earlier state" : drift ? bits(value) + " bits of change" : value.toFixed(1) + "% of uncertainty removed"}`);
    const label = element("span", friendly(name), "name"); label.title = name;
    const track = element("span", undefined, "track");
    const fill = element("span", undefined, "fill");
    fill.style.width = `${value === null ? 0 : Math.min(100, value / limit * 100)}%`;
    track.append(fill);
    button.append(label, track, element("span", value === null ? "∞*" : drift ? bits(value) : value.toFixed(1) + "%", "value"));
    button.addEventListener("click", () => {state.selected = name; renderChart(); const match = Array.from($("bars").children).find(n => n.getAttribute("aria-pressed") === "true"); match?.focus({preventScroll: true});});
    return button;
  }));
  const selected = rows.find(row => nameOf(row) === state.selected);
  if (selected) renderReading(selected);
}
function switchView(view) {
  state.view = view; state.selected = null;
  $("relationships-tab").setAttribute("aria-selected", String(view === "relationships"));
  $("drift-tab").setAttribute("aria-selected", String(view === "drift"));
  $("relationships-tab").tabIndex = view === "relationships" ? 0 : -1;
  $("drift-tab").tabIndex = view === "drift" ? 0 : -1;
  $("analysis-panel").setAttribute("aria-labelledby", view === "relationships" ? "relationships-tab" : "drift-tab");
  renderChart();
}
function countStory(feature, example, info) {
  const target = state.result.report.target;
  if (state.kind === "stocks") return `On days when ${friendly(feature)} moved ${example.state}, ${friendly(target)} moved ${info.event} on ${example.count} of ${example.total} days (${pct(example.rate)}). Across all days, ${friendly(target)} moved ${info.event} ${pct(info.rate)} of the time.`;
  if (state.kind === "weather" && target === "Rain") return `When ${feature.toLowerCase()} was “${example.state}”, it rained in ${example.count} of ${example.total} hours (${pct(example.rate)}). Across all hours, it rained ${pct(info.rate)} of the time.`;
  if (state.kind === "sensor" && target === "Machine condition") return `When ${feature.toLowerCase()} was “${example.state}”, the machine was broken in ${example.count} of ${example.total} checks (${pct(example.rate)}). Across all checks, it was broken ${pct(info.rate)} of the time.`;
  return `When ${friendly(feature)} was “${example.state}”, ${friendly(target)} was “${info.event}” in ${example.count} of ${example.total} observations (${pct(example.rate)}), compared with ${pct(info.rate)} overall.`;
}
function renderStory() {
  const {report, explanation: info} = state.result;
  const top = report.features[0];
  const outcome = state.kind === "stocks" ? `${friendly(report.target)}’s daily movement` : friendly(report.target).toLowerCase();
  if (!report.target_entropy_bits) {
    $("takeaway-title").textContent = `${friendly(report.target)} never changes in this sample.`;
    $("takeaway-body").textContent = `Every observation is “${info.event}”. We need a mix of outcomes to learn which clues distinguish them.`;
  } else if (!top || top.mutual_information_bits < 1e-10) {
    $("takeaway-title").textContent = "No informative clue in this sample.";
    $("takeaway-body").textContent = "The available columns don’t narrow down the outcome. Try a different question or a sample with more relevant measurements.";
  } else {
    const tied = report.features.filter(row => Math.abs(row.mutual_information_bits - top.mutual_information_bits) < 1e-10).length > 1;
    $("takeaway-title").textContent = `${friendly(top.feature)} is ${tied ? "one of the clearest clues" : "the clearest clue"} about ${outcome}.`;
    const example = info.examples[top.feature];
    $("takeaway-body").textContent = example
      ? `${countStory(top.feature, example, info)} ${top.fraction_of_target_information < 0.3 ? "It’s a clue, but most uncertainty remains." : "That difference helps explain why this clue stands out."}`
      : `Of the clues tested, ${friendly(top.feature)} shares the most information with ${outcome}. Its many distinct states can inflate this result; try grouping numeric values in settings.`;
  }
  $("takeaway-limit").textContent = state.kind === "weather"
    ? "These are same-hour patterns in historical weather estimates, not a rain forecast or proof of cause."
    : state.kind === "stocks" ? "These stocks moved on the same days. This does not predict tomorrow’s prices."
    : state.kind === "sensor" ? "This is a made-up lesson: hot always means broken here. The warning light gets 1 in 5 checks wrong. The room tells you nothing. Real machines need real evidence."
    : "This describes this sample. It does not prove cause or accuracy on future observations.";
  $("source-note").hidden = !state.source;
  $("weather-history").hidden = !state.timeline.length;
  if (state.source) {
    const source = state.source;
    $("source-summary").textContent = `Recent: ${source.start} → ${source.end}. Earlier comparison: ${source.reference_start} → ${source.reference_end}. Fetched ${new Date(source.fetched_at).toLocaleString()}${state.cached ? " · reused from the 30-minute local cache" : ""}.`;
    $("source-detail").textContent = source.note;
    $("history-caption").textContent = `${source.start} → ${source.end} · ${state.timeline.reduce((n, day) => n + day.rainy, 0)} rainy hours across ${state.timeline.length} days`;
    $("weather-days").replaceChildren(...state.timeline.map(day => {
      const stripe = element("span", undefined, "weather-day");
      stripe.style.opacity = String(0.12 + 0.88 * day.rainy / day.hours);
      stripe.title = `${day.day}: ${day.rainy} rainy hours out of ${day.hours}`;
      return stripe;
    }));
    $("weather-days").setAttribute("aria-label", state.timeline.map(day => `${day.day}: ${day.rainy} rainy hours`).join("; "));
  }
}
async function calculate() {
  const target = $("target").value;
  const bins = $("bins").value ? Number($("bins").value) : null;
  const result = await request("/api/analyze", {csv: state.csv, reference_csv: state.reference, target, bins});
  state.result = result; state.selected = null;
  $("dataset-title").textContent = state.title;
  $("dataset-description").textContent = state.description;
  $("dataset-meta").textContent = `${result.report.rows.toLocaleString()} ${state.kind === "weather" ? "HOURS" : "OBSERVATIONS"} / EXPLORING ${friendly(target).toUpperCase()}`;
  $("entropy-value").textContent = bits(result.report.target_entropy_bits);
  $("notes").replaceChildren(...result.report.notes.map(note => element("li", note)));
  renderPreview(result.preview); renderDistribution(); renderStory(); renderChart();
}
async function analyze() {
  if (!state.csv || state.busy) return;
  invalidate(); busy(true, "Finding patterns and putting them into words…");
  try {await calculate(); busy(false, "Ready. Read the takeaway, then click a clue to explore it."); if (window.matchMedia('(max-width:720px)').matches) document.querySelector('.results').scrollIntoView({block:'start'});}
  catch (err) {busy(false, "Check the data and try again."); error(err.message);}
}
async function loadDemo(kind) {
  if (state.busy) return;
  invalidate(); busy(true, "Loading and analyzing the example…");
  try {
    const data = await request(`/api/demo?kind=${kind}`);
    state.kind = kind; state.source = null; state.timeline = []; state.cached = false;
    state.csv = data.csv; state.reference = data.reference_csv; state.title = data.title; state.description = data.description;
    const info = await request("/api/preview", {csv: state.csv});
    setColumns(info.columns, data.target); $("bins").value = "";
    ["stocks", "sensor"].forEach(name => {$(name + "-demo").classList.toggle("active", name === kind); $(name + "-demo").setAttribute("aria-pressed", String(name === kind));});
    $("current-name").textContent = data.title + " loaded";
    $("current-file").value = ""; $("reference-file").value = "";
    updateReference(kind === "stocks" ? "Earlier dates included" : "Reference sample included");
    switchView("relationships"); await calculate();
    if (kind === "sensor") {state.selected = "Warning light"; renderChart();}
    busy(false, "Example ready. Read the takeaway, then click a clue.");
    if (window.matchMedia('(max-width:720px)').matches) document.querySelector('.results').scrollIntoView({block:'start'});
  } catch (err) {busy(false, "Unable to load the example."); error(err.message);}
}
async function loadWeather(initial = false) {
  if (state.busy) return;
  invalidate(); busy(true, "Fetching recent weather… then comparing rainy and dry hours. This can take a few seconds.");
  try {
    const data = await request(`/api/weather?city=${encodeURIComponent($("city").value)}`);
    state.kind = "weather"; state.source = data.source; state.timeline = data.timeline; state.cached = data.cached;
    state.csv = data.csv; state.reference = data.reference_csv; state.title = data.title; state.description = data.description;
    const info = await request("/api/preview", {csv: state.csv});
    setColumns(info.columns, data.target); $("bins").value = "";
    ["stocks", "sensor"].forEach(name => {$(name + "-demo").classList.remove("active"); $(name + "-demo").setAttribute("aria-pressed", "false");});
    $("current-name").textContent = data.title + " loaded";
    $("current-file").value = ""; $("reference-file").value = "";
    updateReference("Earlier 45 days included");
    switchView("relationships"); await calculate();
    busy(false, data.cached ? "Ready. Recent weather is reused for 30 minutes to avoid unnecessary requests." : "Weather fetched. Here’s what the data says.");
    if (!initial && window.matchMedia('(max-width:720px)').matches) document.querySelector('.results').scrollIntoView({block:'start'});
  } catch (err) {
    state.csv = ""; state.reference = ""; state.source = null; state.timeline = [];
    $("dataset-title").textContent = "The weather source is unavailable.";
    $("dataset-description").textContent = "You can still explore the stock study or device lesson. Both are included in the app.";
    $("dataset-meta").textContent = "NO WEATHER RESULT";
    $("takeaway-title").textContent = "Try a built-in story while we’re offline.";
    $("takeaway-body").textContent = "Choose the warning-light story for a quick explanation with a known answer, or retry the weather request.";
    $("current-name").textContent = "No weather loaded";
    $("table-head").replaceChildren(); $("table-body").replaceChildren();
    $("preview-summary").textContent = "No observations loaded";
    busy(false, "Weather wasn’t loaded. No example data is being presented as fresh weather."); error(err.message);
  }
}
async function loadFile(file, reference = false) {
  if (!file || state.busy) return;
  if (file.size > 3 * 1024 * 1024) {error("Choose a CSV smaller than 3 MB."); return;}
  busy(true, "Reading the CSV…"); error("");
  try {
    const text = await file.text();
    const info = await request("/api/preview", {csv: text});
    if (reference) {state.reference = text; updateReference(file.name);}
    else {
      state.kind = "custom"; state.source = null; state.timeline = [];
      state.csv = text; state.reference = ""; state.title = file.name; state.description = "Your observations. Choose an outcome and explore its relationships.";
      setColumns(info.columns, $("target").value); $("bins").value = "";
      $("current-name").textContent = file.name;
      $("reference-file").value = ""; updateReference("No reference sample");
      ["stocks", "sensor"].forEach(name => {$(name + "-demo").classList.remove("active"); $(name + "-demo").setAttribute("aria-pressed", "false");});
      $("dataset-title").textContent = file.name;
      $("dataset-description").textContent = state.description;
      $("dataset-meta").textContent = `${info.rows.toLocaleString()} OBSERVATIONS / ${info.columns.length} COLUMNS`;
      renderPreview(info);
    }
    busy(false); invalidate(info.missing ? `CSV loaded with ${info.missing} missing values. Clean these before analysis.` : "CSV loaded. Choose your target, then analyze signals.");
  } catch (err) {busy(false, "The previous data is still loaded."); error(err.message);}
}
function download(name, content, type) {
  const url = URL.createObjectURL(new Blob([content], {type}));
  const anchor = element("a"); anchor.href = url; anchor.download = name;
  document.body.append(anchor); anchor.click(); anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
$("stocks-demo").addEventListener("click", () => loadDemo("stocks"));
$("sensor-demo").addEventListener("click", () => loadDemo("sensor"));
$("analyze").addEventListener("click", analyze);
$("weather-load").addEventListener("click", () => loadWeather());
$("shuffle-clue").addEventListener("click", async () => {
  if (!state.result || state.busy || !state.selected) return;
  busy(true, "Mixing up the selected clue’s rows and recalculating…");
  try {
    const result = await request("/api/shuffle", {csv: state.csv, target: $("target").value, bins: $("bins").value ? Number($("bins").value) : null, feature: state.selected});
    const lines = [["Original pairs", result.before_fraction], ["Mixed-up pairs", result.after_fraction]].map(([label, value]) => {
      const line = element("div", undefined, "shuffle-comparison");
      const track = element("div", undefined, "shuffle-track");
      const fill = element("div", undefined, "shuffle-fill"); fill.style.width = `${value * 100}%`; track.append(fill);
      line.append(element("span", label), track, element("strong", pct(value))); return line;
    });
    $("shuffle-result").replaceChildren(...lines, element("p", `${friendly(result.feature)} removes ${pct(result.before_fraction)} of the uncertainty with the original pairings, and ${pct(result.after_fraction)} after mixing them up. The individual counts are unchanged. Information depends on how things line up, not just how often they happen.`), element("p", result.note));
    $("shuffle-result").hidden = false;
    busy(false, "Experiment complete. The original data and findings above are unchanged.");
  } catch (err) {busy(false, "Could not run the experiment."); error(err.message);}
});
$("city").addEventListener("change", () => loadWeather());
$("target").addEventListener("change", analyze);
$("bins").addEventListener("change", analyze);
$("current-file").addEventListener("change", event => loadFile(event.target.files[0]));
$("reference-file").addEventListener("change", event => loadFile(event.target.files[0], true));
$("remove-reference").addEventListener("click", () => {state.reference = ""; $("reference-file").value = ""; updateReference("No reference sample"); invalidate();});
$("relationships-tab").addEventListener("click", () => switchView("relationships"));
$("drift-tab").addEventListener("click", () => switchView("drift"));
document.querySelector(".tabs").addEventListener("keydown", event => {
  if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) {
    event.preventDefault(); const next = event.key === "Home" ? "relationships" : event.key === "End" ? "drift" : state.view === "drift" ? "relationships" : "drift";
    switchView(next); $(next === "drift" ? "drift-tab" : "relationships-tab").focus();
  }
});
$("download-report").addEventListener("click", () => {if (state.result) download("entropy-audit.json", JSON.stringify({...state.result.report, explanation: state.result.explanation, takeaway: $("takeaway-title").textContent, source: state.source}, null, 2), "application/json");});
$("download-data").addEventListener("click", () => {if (state.csv) download("observations.csv", state.csv, "text/csv");});
$("help-open").addEventListener("click", () => $("help").showModal());
$("help-close").addEventListener("click", () => $("help").close());
const drop = $("drop-current");
["dragenter", "dragover"].forEach(event => drop.addEventListener(event, e => {e.preventDefault(); if (!state.busy) drop.classList.add("dragover");}));
["dragleave", "drop"].forEach(event => drop.addEventListener(event, e => {e.preventDefault(); drop.classList.remove("dragover");}));
drop.addEventListener("drop", e => loadFile(e.dataTransfer.files[0]));
loadWeather(true);
