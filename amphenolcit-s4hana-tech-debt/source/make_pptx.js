const pptxgen = require("pptxgenjs");
const React = require("react");
const RDS = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const OUT = process.argv[2];
const C = {
  dark: "17313B", teal: "0F766E", teal2: "14B8A6", tint: "E6F2F0", amber: "F59E0B", amberT: "FEF3C7",
  text: "1F2937", muted: "6B7280", line: "D1D5DB", white: "FFFFFF", grey: "F3F4F6",
  red: "BE123C", purple: "7C3AED", blue: "1D4ED8", brown: "B45309", slate: "475569",
};
const HF = "Arial", BF = "Calibri";

async function icon(name, color = "FFFFFF", size = 256) {
  const svg = RDS.renderToStaticMarkup(React.createElement(fa[name], { color: "#" + color, size }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
  pres.title = "AmphenolCIT S/4HANA Tech Debt & Innovation Strategy";
  const W = 13.333;

  const ICONS = {};
  for (const n of ["FaDesktop", "FaRocket", "FaProjectDiagram", "FaDatabase", "FaTable", "FaCode", "FaSitemap", "FaServer",
    "FaVial", "FaSearch", "FaClipboardList", "FaChartLine", "FaCogs", "FaBolt", "FaFlag", "FaLayerGroup", "FaBalanceScale",
    "FaSyncAlt", "FaEye", "FaQuestion", "FaCheck", "FaUsers", "FaCompass", "FaTools", "FaCalendarAlt", "FaCoins"]) {
    ICONS[n] = await icon(n);
  }

  const T = (s, text, x, y, w, h, o = {}) => s.addText(text, {
    x, y, w, h, fontFace: o.fontFace || BF, fontSize: o.fontSize || 14, color: o.color || C.text, bold: o.bold,
    italic: o.italic, align: o.align || "left", valign: o.valign || "top", margin: o.margin ?? 0, isTextBox: true,
    paraSpaceAfter: o.paraSpaceAfter, lineSpacingMultiple: o.lsm, fit: o.fit,
  });
  const title = (s, text, lead) => {
    T(s, text, 0.6, 0.4, 12.1, 0.75, { fontFace: HF, fontSize: 30, bold: true, color: C.dark, valign: "middle" });
    if (lead) T(s, lead, 0.6, 1.15, 12.1, 0.45, { fontSize: 16, color: C.muted, valign: "middle" });
  };
  const circle = (s, ic, x, y, d, fill = C.teal) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
    const p = d * 0.26;
    s.addImage({ data: ICONS[ic], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p });
  };
  const card = (s, x, y, w, h, fill = C.white, shadow = true) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill === C.white ? "E5E7EB" : fill, width: 0.75 },
    shadow: shadow ? { type: "outer", color: "000000", blur: 6, offset: 2, angle: 90, opacity: 0.12 } : undefined,
  });
  const bullets = (items, o = {}) => items.map((it, i) => {
    const parts = Array.isArray(it) ? it : [it];
    return parts.map((p, j) => ({
      text: typeof p === "string" ? p : p[0],
      options: { bold: typeof p !== "string", bullet: j === 0 ? (o.bullet === false ? false : { indent: 14 }) : undefined,
        breakLine: j === parts.length - 1 && i < items.length - 1, fontSize: o.fontSize, color: o.color },
    }));
  }).flat();
  const footer = (s, n) => T(s, `AmphenolCIT  |  S/4HANA Tech Debt & Innovation Strategy  |  Draft for discussion   ${n}`, 0.6, 7.05, 12.1, 0.3, { fontSize: 9, color: "9CA3AF", align: "right" });

  // ---------------------------------------------------------------- 1 Title
  let s = pres.addSlide(); let n = 1;
  s.background = { color: C.dark };
  s.addShape(pres.shapes.OVAL, { x: 8.9, y: -1.2, w: 6.2, h: 6.2, fill: { color: C.teal, transparency: 55 }, line: { color: C.teal, transparency: 55 } });
  s.addShape(pres.shapes.OVAL, { x: 10.6, y: 3.7, w: 3.6, h: 3.6, fill: { color: C.teal2, transparency: 70 }, line: { color: C.teal2, transparency: 70 } });
  circle(s, "FaRocket", 10.9, 1.35, 1.9, C.amber);
  T(s, "AMPHENOLCIT  |  ENTERPRISE ARCHITECTURE", 0.8, 1.3, 8, 0.4, { fontSize: 13, color: C.teal2, bold: true });
  T(s, "From go-live to value", 0.8, 1.9, 8.5, 1.1, { fontFace: HF, fontSize: 48, bold: true, color: C.white });
  T(s, "A plan to pay down S/4HANA technical debt and unlock Fiori, SAP Build Work Zone, Integration Suite and trusted data — without breaking the budget", 0.8, 3.1, 7.8, 1.3, { fontSize: 20, color: "CBD5E1" });
  T(s, "Draft for discussion  |  September 2026", 0.8, 5.9, 6, 0.4, { fontSize: 13, color: "94A3B8" });
  s.addNotes("Purpose: agree how AmphenolCIT will plan, prioritise and fund post-go-live technical debt alongside new functionality. The deck is paired with a Planner workbook (backlog, capacity, roadmap, KPIs) and a Quick Reference Guide for collecting tech debt. All numbers are placeholders until discovery is complete.");

  // ---------------------------------------------------------------- 2 What we heard
  s = pres.addSlide(); n++;
  title(s, "One year after go-live: the platform is live, the value isn’t yet", "What we heard from the team");
  const heard = [
    ["FaDesktop", "Fiori not in use", "Users still on SAP GUI; role-based Fiori apps and launchpad not rolled out."],
    ["FaRocket", "Hungry for innovation", "Strong demand for the latest S/4HANA functions and SAP Build Work Zone."],
    ["FaProjectDiagram", "Integration Suite: early days", "Usage just started; standards, monitoring and a migration plan are not yet in place."],
    ["FaDatabase", "Data quality issues", "Errors and low trust in reports; data quality is not measured or owned."],
    ["FaTable", "Custom fields hold the data", "Business data sits in Z-fields that standard Fiori apps, APIs and analytics cannot see."],
  ];
  const cw = 2.3, gap = 0.2, x0 = 0.6;
  heard.forEach(([ic, h, d], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, 1.9, cw, 3.3);
    circle(s, ic, x + 0.25, 2.15, 0.75);
    T(s, h, x + 0.25, 3.05, cw - 0.5, 0.65, { fontSize: 16, bold: true, color: C.dark });
    T(s, d, x + 0.25, 3.7, cw - 0.5, 1.4, { fontSize: 13, color: C.text });
  });
  card(s, 0.6, 5.5, 12.1, 1.25, C.tint, false);
  T(s, [
    { text: "The pattern: ", options: { bold: true, color: C.teal } },
    { text: "scope deferred to “phase 2” at go-live has become debt that charges interest every month — manual workarounds, invisible data, fragile interfaces — and it blocks the innovation the business is asking for. The fix is a managed, continuous backlog, not another big project." },
  ], 0.85, 5.6, 11.6, 1.05, { fontSize: 15, valign: "middle" });
  footer(s, n);
  s.addNotes("Summarise the interviews. The five symptoms are connected: Z-field data and missing Fiori roles are why standard apps look empty; weak integration monitoring and missing data ownership drive the data quality issues. Treat them as one programme with one backlog.");

  // ---------------------------------------------------------------- 3 Tech debt definition & categories
  s = pres.addSlide(); n++;
  title(s, "What we mean by technical debt in S/4HANA", "Anything that works today but makes change slower, riskier or impossible tomorrow");
  card(s, 0.6, 1.9, 3.7, 4.85, C.dark, false);
  T(s, "Principal & interest", 0.85, 2.1, 3.2, 0.5, { fontSize: 18, bold: true, color: C.white });
  T(s, bullets([
    [["Principal: "], "the one-off effort to fix it."],
    [["Interest: "], "what it costs every month we keep it — workarounds, incidents, extra testing, blocked features."],
    [["Rule: "], "pay down debt with high interest and low principal first; accept and document the rest."],
  ]), 0.85, 2.7, 3.25, 2.6, { fontSize: 14, color: "E2E8F0", paraSpaceAfter: 8 });
  T(s, "Every register item records both, so debt competes on value, not on noise.", 0.85, 5.55, 3.25, 1.0, { fontSize: 13, italic: true, color: C.teal2 });
  const cats = [
    ["FaCode", "Custom code & modifications", "Z-objects, user-exit code, unused code", "Extensibility"],
    ["FaDesktop", "User experience", "GUI-only, no Fiori roles, many entry points", "UX"],
    ["FaProjectDiagram", "Integration", "Point-to-point, unmonitored IDoc/RFC/file", "Integration"],
    ["FaTable", "Data & custom fields", "Z-field data, duplicates, no data owners", "Data"],
    ["FaSitemap", "Process workarounds", "Excel steps, re-keying, unused standard", "Processes"],
    ["FaServer", "Platform & operations", "Release lag, manual transports, no tests", "Operations"],
  ];
  cats.forEach(([ic, h, d, dim], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 4.6 + col * 4.1, y = 1.9 + row * 1.65;
    card(s, x, y, 3.95, 1.5);
    circle(s, ic, x + 0.2, y + 0.3, 0.8);
    T(s, h, x + 1.2, y + 0.18, 2.6, 0.4, { fontSize: 15, bold: true, color: C.dark });
    T(s, d, x + 1.2, y + 0.57, 2.6, 0.5, { fontSize: 12 });
    T(s, "Clean core: " + dim, x + 1.2, y + 1.07, 2.6, 0.3, { fontSize: 11, color: C.teal, bold: true });
  });
  footer(s, n);
  s.addNotes("Use this vocabulary in every conversation. The six categories map to SAP's five clean core dimensions plus user experience. Section 2 of the Quick Reference Guide lists the symptoms, evidence sources and fix patterns per category.");

  // ---------------------------------------------------------------- 4 Clean core
  s = pres.addSlide(); n++;
  title(s, "SAP’s answer: keep the core clean, extend on the side", "SAP clean core dimensions, with our initial gap assessment (to be validated in discovery)");
  const dims = [
    ["Processes", "Standard, best-practice processes; fit-to-standard", "M"],
    ["Extensibility", "Released APIs, ABAP Cloud, key-user and BTP side-by-side extensions", "H"],
    ["Data", "Owned, governed, high-quality master and transactional data", "H"],
    ["Integration", "Standard APIs/events, central middleware and monitoring", "H"],
    ["Operations", "Current release, automated test, transport and monitoring", "M"],
  ];
  T(s, "Dimension", 0.6, 1.85, 2.0, 0.3, { fontSize: 12, bold: true, color: C.muted });
  T(s, "What “clean” looks like", 2.7, 1.85, 4.2, 0.3, { fontSize: 12, bold: true, color: C.muted });
  T(s, "Gap", 6.95, 1.85, 0.6, 0.3, { fontSize: 12, bold: true, color: C.muted, align: "center" });
  dims.forEach(([d, t, g], i) => {
    const y = 2.2 + i * 0.9;
    card(s, 0.6, y, 7.0, 0.78, i % 2 ? C.grey : C.white, false);
    T(s, d, 0.8, y, 1.9, 0.78, { fontSize: 15, bold: true, color: C.dark, valign: "middle" });
    T(s, t, 2.7, y, 4.1, 0.78, { fontSize: 13, valign: "middle" });
    const col = g === "H" ? C.red : C.amber;
    s.addShape(pres.shapes.OVAL, { x: 7.05, y: y + 0.2, w: 0.38, h: 0.38, fill: { color: col }, line: { color: col } });
    T(s, g, 7.05, y + 0.2, 0.38, 0.38, { fontSize: 11, bold: true, color: C.white, align: "center", valign: "middle" });
  });
  T(s, "H = high gap, M = medium gap. Hypothesis from interviews only.", 0.6, 6.7, 7, 0.3, { fontSize: 10, italic: true, color: C.muted });
  // A-D ladder
  T(s, "Extensibility levels A–D", 8.1, 1.8, 4.6, 0.4, { fontSize: 16, bold: true, color: C.dark });
  const lv = [["A", "Released APIs, ABAP Cloud, key-user, BTP", "Target for all new work", C.teal],
    ["B", "Classic APIs SAP lists as stable", "Acceptable; monitor", C.teal2],
    ["C", "Internal / unreleased SAP objects", "Remediate when touched", C.amber],
    ["D", "Modifications, implicit enhancements", "Retire or refactor first", C.red]];
  lv.forEach(([l, d, a, col], i) => {
    const y = 2.3 + i * 1.08;
    card(s, 8.1, y, 4.6, 0.95);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.2, y: y + 0.12, w: 0.7, h: 0.7, rectRadius: 0.08, fill: { color: col }, line: { color: col } });
    T(s, l, 8.2, y + 0.12, 0.7, 0.7, { fontFace: HF, fontSize: 24, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, d, 9.1, y + 0.1, 3.5, 0.4, { fontSize: 13, bold: true, color: C.dark });
    T(s, a, 9.1, y + 0.5, 3.5, 0.35, { fontSize: 12, color: C.muted });
  });
  T(s, "Per SAP’s current extensibility guidance; confirm against the latest version.", 8.1, 6.7, 4.6, 0.3, { fontSize: 10, italic: true, color: C.muted });
  footer(s, n);
  s.addNotes("SAP frames post-go-live health as 'clean core' across five dimensions. For code, SAP's current guidance grades each extension A (released, upgrade-stable) to D (modifications). Our KPI will be the trend of C and D items and the share of new work built at level A. For custom fields, the Custom Fields app (key-user extensibility) is level A and exposes the field to CDS, OData and Fiori automatically.");

  // ---------------------------------------------------------------- 5 SAP tools
  s = pres.addSlide(); n++;
  title(s, "SAP tooling to discover, plan, build and measure", "Most of this is already included in SAP Enterprise Support / RISE or is free — confirm entitlements");
  const cols = [
    ["FaSearch", "Discover", ["SAP Readiness Check (release / FPS upgrade)", "Innovation & Optimization Pathfinder (usage-based Fiori & feature recommendations)", "Signavio Process Insights (process KPIs, improvement hints)", "ATC with clean-core checks; SCMON / SUSG usage", "Integration Suite Migration Assessment"]],
    ["FaClipboardList", "Plan & govern", ["SAP Cloud ALM: requirements, user stories, backlog, roadmap", "SAP LeanIX: application & tech-debt portfolio (if licensed)", "SAP Activate (Run phase, continuous improvement)", "ISA-M for integration patterns", "Clean core guidance & BTP Guidance Framework"]],
    ["FaTools", "Build & run", ["Fiori launchpad, spaces & pages, Fiori Apps Reference Library", "SAP Build Work Zone (standard / advanced)", "Integration Suite; Cloud Connector; Cloud Identity Services", "Custom Fields app; ABAP Cloud / RAP; CAP on BTP", "MDG / data quality rules; Build Process Automation"]],
    ["FaChartLine", "Monitor & measure", ["Cloud ALM: integration & exception, job, health monitoring", "Cloud ALM test management & Change and Deployment", "Fiori / Work Zone usage analytics", "Custom Code Migration app trends", "SAP Enterprise Support / Preferred Success services"]],
  ];
  cols.forEach(([ic, h, items], i) => {
    const x = 0.6 + i * 3.1, w = 2.9;
    card(s, x, 1.9, w, 4.9);
    circle(s, ic, x + 0.2, 2.05, 0.65);
    T(s, h, x + 1.0, 2.05, w - 1.1, 0.65, { fontSize: 17, bold: true, color: C.dark, valign: "middle" });
    T(s, bullets(items), x + 0.2, 2.9, w - 0.35, 3.8, { fontSize: 12.5, paraSpaceAfter: 7 });
  });
  footer(s, n);
  s.addNotes("Start with the free / included tools: Readiness Check, Pathfinder (upload ST03N usage to get Fiori app recommendations), ATC clean-core checks, SCMON/SUSG for unused code, Cloud ALM for backlog, testing and monitoring. LeanIX, Signavio and MDG depend on licences - to be confirmed. Ask the SAP account team / CSP about Enterprise Support or Preferred Success services that can run parts of discovery at no extra cost.");

  // ---------------------------------------------------------------- 6 Frameworks
  s = pres.addSlide(); n++;
  title(s, "Proven frameworks we borrow — lightly", "Use the parts that solve our problem; avoid framework overhead");
  const fw = [
    ["FaBalanceScale", "Flow Framework", "Four work types (features, defects, risks, debts) and flow distribution — shows where capacity really goes."],
    ["FaLayerGroup", "SAFe WSJF & capacity allocation", "Rank by cost of delay ÷ size; set % guardrails per work type each quarter."],
    ["FaCompass", "Fowler tech-debt quadrant", "Deliberate vs inadvertent, prudent vs reckless — explains why debt exists and stops repeats."],
    ["FaSyncAlt", "Kanban flow metrics", "WIP limits, lead time, throughput, aging items — simple visible progress."],
    ["FaBolt", "DORA metrics", "Deployment frequency, lead time, change failure rate, restore time — for BTP / integration delivery."],
    ["FaUsers", "TOGAF-style design authority", "Architecture board approves extension and integration patterns; prevents new debt."],
    ["FaCogs", "ITIL 4 problem management", "Turns repeat incidents into root-cause backlog items instead of recurring tickets."],
    ["FaTools", "Delivery tools", "Cloud ALM, Jira / Azure DevOps or ServiceNow SPM for the board; Tricentis or Cloud ALM for test automation."],
  ];
  fw.forEach(([ic, h, d], i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = 0.6 + col * 3.1, y = 1.9 + row * 2.5, w = 2.9;
    card(s, x, y, w, 2.3);
    circle(s, ic, x + 0.2, y + 0.2, 0.6);
    T(s, h, x + 0.95, y + 0.2, w - 1.05, 0.6, { fontSize: 14, bold: true, color: C.dark, valign: "middle" });
    T(s, d, x + 0.2, y + 0.95, w - 0.4, 1.3, { fontSize: 12.5 });
  });
  footer(s, n);
  s.addNotes("We are not adopting full SAFe. We borrow WSJF and capacity allocation from SAFe, work types and flow distribution from the Flow Framework, and the Fowler quadrant to classify root causes. The board can live in Cloud ALM (included) or the existing enterprise tool (Jira / Azure DevOps / ServiceNow) - pick the one the IT team already uses.");

  // ---------------------------------------------------------------- 7 Flow of work
  s = pres.addSlide(); n++;
  title(s, "How work flows to the IT team", "One front door, clear gates, and an expedite lane for production issues");
  const steps = [
    ["Intake", "Anyone", "Request, incident, ATC / monitoring finding logged"],
    ["Triage", "PO + leads, weekly", "Type, dimension, severity; duplicates closed"],
    ["Refine", "PO + architects", "Sized, WSJF, owners → Definition of Ready"],
    ["Prioritise", "Portfolio, monthly", "Ranked inside capacity guardrails"],
    ["Plan", "Team, bi-weekly", "Sprint goal; mix per allocation %"],
    ["Build & test", "Delivery team", "Design authority for new extensions; automated regression"],
    ["Release", "Change board", "Transport / cTMS; release notes"],
    ["Measure", "PO + EA", "KPIs, demo, feedback into backlog"],
  ];
  const sw = 1.5, sx = 0.6;
  steps.forEach(([h, who, d], i) => {
    const x = sx + i * (sw + 0.02);
    s.addShape(i === 0 ? pres.shapes.PENTAGON : pres.shapes.CHEVRON, { x, y: 1.95, w: sw, h: 0.85, fill: { color: i % 2 ? C.teal : C.dark }, line: { color: C.white, width: 1 } });
    T(s, h, x + 0.22, 1.95, sw - 0.34, 0.85, { fontSize: 11.5, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, who, x + 0.05, 2.95, sw - 0.1, 0.35, { fontSize: 11, bold: true, color: C.teal, align: "center" });
    T(s, d, x + 0.05, 3.3, sw - 0.1, 1.1, { fontSize: 11, align: "center" });
  });
  card(s, 0.6, 4.55, 12.1, 0.8, C.amberT, false);
  circle(s, "FaBolt", 0.8, 4.65, 0.6, C.amber);
  T(s, [{ text: "Expedite lane: ", options: { bold: true } }, { text: "P1 / P2 defects skip triage and ranking, are swarmed immediately and funded from the defect allocation. Everything else waits its turn." }], 1.6, 4.55, 10.9, 0.8, { fontSize: 14, valign: "middle" });
  const gates = [["Definition of Ready", "Business owner named, acceptance criteria, WSJF scored, clean core level and design approved, test data known."],
    ["Definition of Done", "Tested (automated where possible), documented in Cloud ALM, no new level C/D code without waiver, KPI impact recorded."]];
  gates.forEach(([h, d], i) => {
    const x = 0.6 + i * 6.15;
    card(s, x, 5.55, 5.95, 1.3);
    circle(s, "FaCheck", x + 0.2, 5.75, 0.55);
    T(s, h, x + 0.95, 5.65, 4.8, 0.4, { fontSize: 14, bold: true, color: C.dark });
    T(s, d, x + 0.95, 6.05, 4.85, 0.75, { fontSize: 12 });
  });
  footer(s, n);
  s.addNotes("One front door stops side-channel requests. Weekly triage keeps the backlog clean; refinement makes items Ready; the monthly portfolio review decides what gets capacity. The design authority step is how we stop creating new debt while paying down the old. Definitions of Ready and Done make the gates explicit.");

  // ---------------------------------------------------------------- 8 One backlog
  s = pres.addSlide(); n++;
  title(s, "One backlog, five work types", "Everything competes for the same capacity — so trade-offs become visible");
  const hier = [["Theme", "Clean core dimension, e.g. Data"], ["Epic", "Custom-field remediation for material master"], ["Feature", "Expose Z-fields via Custom Fields app"], ["Story / task", "Map ZZ_REGION to standard field; test; migrate"]];
  hier.forEach(([h, d], i) => {
    const x = 0.6 + i * 0.35, y = 1.95 + i * 1.18, w = 5.2 - i * 0.35;
    card(s, x, y, w, 1.0, i === 0 ? C.dark : (i === 1 ? C.teal : (i === 2 ? C.tint : C.white)), i > 1);
    T(s, h, x + 0.2, y + 0.1, w - 0.4, 0.35, { fontSize: 14, bold: true, color: i < 2 ? C.white : C.dark });
    T(s, d, x + 0.2, y + 0.48, w - 0.4, 0.45, { fontSize: 12, color: i < 2 ? "E2E8F0" : C.text });
  });
  const types = [["Feature", "New capability, e.g. Fiori wave, Work Zone site", C.teal],
    ["Defect", "Doesn’t work as designed; P1–P4", C.red],
    ["Tech debt", "Works but slows / blocks change; has interest", C.purple],
    ["Enabler", "Platform work others depend on, e.g. landing zone", C.blue],
    ["Risk / compliance", "Security, audit, maintenance deadlines", C.brown]];
  T(s, "Work types", 6.5, 1.85, 6, 0.4, { fontSize: 16, bold: true, color: C.dark });
  types.forEach(([h, d, col], i) => {
    const y = 2.3 + i * 0.7;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.5, y, w: 1.9, h: 0.55, rectRadius: 0.08, fill: { color: col }, line: { color: col } });
    T(s, h, 6.5, y, 1.9, 0.55, { fontSize: 13, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, d, 8.55, y, 4.2, 0.55, { fontSize: 13, valign: "middle" });
  });
  card(s, 6.5, 5.95, 6.2, 0.9, C.tint, false);
  T(s, [{ text: "Every item carries: ", options: { bold: true, color: C.teal } }, { text: "dimension, clean core level, interest, principal, WSJF inputs, business + IT owner, target quarter. See Planner → Tech Debt Register." }], 6.7, 5.95, 5.9, 0.9, { fontSize: 13, valign: "middle" });
  footer(s, n);
  s.addNotes("A separate tech-debt list never gets prioritised. By putting all five work types in one ranked backlog, the business sees that choosing a new feature means deferring a debt item, and vice versa. The hierarchy links sprint-level tasks up to clean core themes, so progress rolls up to leadership KPIs.");

  // ---------------------------------------------------------------- 9 Prioritisation
  s = pres.addSlide(); n++;
  title(s, "Prioritising bugs vs features vs tech debt", "Three decisions, made at three different levels");
  const lvls = [["1", "Expedite", "P1 / P2 defects and security issues go first. Non-negotiable, but capped by the defect allocation; overflow triggers a portfolio conversation.", "Daily"],
    ["2", "Allocate", "Portfolio sets % of capacity per work type each quarter (next slide). This is the budget decision, made once — not item by item.", "Monthly / quarterly"],
    ["3", "Rank", "Inside each bucket, rank by WSJF. Tech debt scores on risk reduction and opportunity enablement, not just business value.", "Weekly refinement"]];
  lvls.forEach(([num, h, d, cad], i) => {
    const y = 1.9 + i * 1.6;
    card(s, 0.6, y, 7.1, 1.45);
    s.addShape(pres.shapes.OVAL, { x: 0.8, y: y + 0.35, w: 0.75, h: 0.75, fill: { color: C.dark }, line: { color: C.dark } });
    T(s, num, 0.8, y + 0.35, 0.75, 0.75, { fontFace: HF, fontSize: 24, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, h, 1.8, y + 0.12, 3.5, 0.4, { fontSize: 17, bold: true, color: C.dark });
    T(s, cad, 4.9, y + 0.14, 2.6, 0.4, { fontSize: 12, bold: true, color: C.teal, align: "right" });
    T(s, d, 1.8, y + 0.52, 5.7, 0.9, { fontSize: 12.5 });
  });
  card(s, 8.0, 1.9, 4.7, 1.45, C.amberT, false);
  T(s, "WSJF", 8.2, 2.0, 4.3, 0.35, { fontSize: 13, bold: true, color: C.brown });
  T(s, "(Business value + Time criticality + Risk reduction / Opportunity enablement) ÷ Job size", 8.2, 2.35, 4.3, 0.95, { fontSize: 14, bold: true, color: C.dark });
  // 2x2 interest vs principal
  T(s, "Tech debt: interest vs principal", 8.0, 3.55, 4.7, 0.35, { fontSize: 14, bold: true, color: C.dark });
  const q = [["Pay down now", "High interest, low principal", C.teal, C.white], ["Plan an epic", "High interest, high principal", C.teal2, C.white],
    ["Fix when touched", "Low interest, low principal", C.tint, C.dark], ["Accept & document", "Low interest, high principal", C.grey, C.dark]];
  q.forEach(([h, d, f, tc], i) => {
    const x = 8.4 + (i % 2) * 2.17, y = 3.95 + Math.floor(i / 2) * 1.35;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.12, h: 1.3, fill: { color: f }, line: { color: C.white, width: 1 } });
    T(s, h, x + 0.1, y + 0.2, 1.92, 0.4, { fontSize: 14, bold: true, color: tc, align: "center" });
    T(s, d, x + 0.1, y + 0.62, 1.92, 0.55, { fontSize: 11, color: tc, align: "center" });
  });
  T(s, "Interest ↑", 7.95, 4.3, 0.45, 1.8, { fontSize: 10, color: C.muted, align: "center", valign: "middle" });
  T(s, "Principal →", 8.4, 6.67, 4.3, 0.3, { fontSize: 10, color: C.muted, align: "center" });
  footer(s, n);
  s.addNotes("Separating the three decisions stops every item turning into a debate. Leadership decides the split once per quarter; the team ranks within it. WSJF uses a Fibonacci scale 1-20 - the scoring anchors are in the Quick Reference Guide, section 5. For tech debt, the interest/principal grid is a quick sanity check on the WSJF result.");

  // ---------------------------------------------------------------- 10 Capacity guardrails
  s = pres.addSlide(); n++;
  title(s, "Capacity guardrails keep the budget flat", "Fund a stable team, then shift the mix as debt comes down (illustrative %)");
  const qs = ["Q4-26", "Q1-27", "Q2-27", "Q3-27", "Q4-27"];
  const alloc = { Feature: [30, 35, 40, 45, 50], Defect: [20, 15, 15, 15, 15], "Tech debt": [25, 25, 25, 20, 20], Enabler: [20, 20, 15, 15, 10], "Risk/compliance": [5, 5, 5, 5, 5] };
  s.addChart(pres.charts.BAR, Object.entries(alloc).map(([name, values]) => ({ name, labels: qs, values })), {
    x: 0.6, y: 1.8, w: 6.9, h: 5.1, barDir: "col", barGrouping: "percentStacked", barGapWidthPct: 60,
    chartColors: [C.teal, C.red, C.purple, C.blue, C.brown],
    showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 10, dataLabelFormatCode: "0",
    showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: BF,
    catAxisLabelColor: C.muted, valAxisLabelColor: C.muted, valAxisLabelFontSize: 10, catAxisLabelFontSize: 11,
    valAxisLabelFormatCode: "0%", valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showTitle: true, title: "Share of team capacity by work type (%)", titleFontSize: 13, titleColor: C.dark, titleFontFace: BF,
  });
  T(s, "Funding tactics that don’t need new budget", 7.9, 1.85, 4.8, 0.4, { fontSize: 16, bold: true, color: C.dark });
  T(s, bullets([
    [["Stable team, flexible mix: "], "fund capacity once; the portfolio moves the % each quarter."],
    [["Bundle: "], "fix debt in the objects a feature already touches (Boy Scout rule)."],
    [["Retire before remediate: "], "unused code and interfaces cost nothing to delete."],
    [["Use what’s paid for: "], "Cloud ALM, Pathfinder, Readiness Check, BTP credits, Enterprise Support services."],
    [["Self-fund: "], "redeploy savings from fewer tickets, retired middleware and AMS effort."],
    [["Stage-gate epics: "], "release funding in slices tied to KPI movement."],
  ]), 7.9, 2.35, 4.8, 4.5, { fontSize: 13, paraSpaceAfter: 8 });
  footer(s, n);
  s.addNotes("Front-load enablers and tech debt while the foundation is built (Work Zone, Integration Suite landing zone, Fiori roles, custom-field clean-up), then shift toward features as the platform stabilises. Keep tech debt + enablers at or above ~25-30% while clean core KPIs are red. The Planner's Capacity & Budget tab compares these guardrails with live demand from the register.");

  // ---------------------------------------------------------------- 11 Cadence
  s = pres.addSlide(); n++;
  title(s, "Grooming and repetition: the operating cadence", "Same meetings, same day, every cycle — the rhythm is what makes the backlog trustworthy");
  const cad = [["Daily", ["Stand-up (15 min)"], C.slate],
    ["Weekly", ["Intake triage (45 min)", "Backlog refinement (60–90 min)"], C.teal],
    ["Bi-weekly", ["Sprint planning", "Sprint review / demo with users", "Retrospective", "Design authority"], C.teal2],
    ["Monthly", ["Portfolio & capacity review", "KPI dashboard to leadership"], C.blue],
    ["Quarterly", ["Roadmap refresh / PI planning", "Tech debt register health check"], C.purple],
    ["Semi-annual", ["SAP innovation scan (release notes, Pathfinder, Fiori app library)"], C.brown]];
  cad.forEach(([f, items, col], i) => {
    const y = 1.85 + i * 0.83;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 1.8, h: 0.68, rectRadius: 0.08, fill: { color: col }, line: { color: col } });
    T(s, f, 0.6, y, 1.8, 0.68, { fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle" });
    let x = 2.6;
    items.forEach(it => {
      const w = Math.max(2.1, it.length * 0.085 + 0.4);
      card(s, x, y + 0.04, w, 0.6, C.white);
      T(s, it, x + 0.1, y + 0.04, w - 0.2, 0.6, { fontSize: 12, align: "center", valign: "middle" });
      x += w + 0.15;
    });
  });
  T(s, "Details, participants, inputs and outputs: Planner → Cadence tab.", 0.6, 6.85, 8, 0.25, { fontSize: 10, italic: true, color: C.muted });
  footer(s, n);
  s.addNotes("Repetition is the point. Weekly triage and refinement keep the top of the backlog Ready; the bi-weekly demo shows users progress; the monthly portfolio review is where the capacity split and budget are checked; the quarterly health check closes stale items and re-scores debt. The semi-annual innovation scan feeds new S/4 and BTP features into the backlog so the business sees innovation, not only fixes.");

  // ---------------------------------------------------------------- 12 Visible progress
  s = pres.addSlide(); n++;
  title(s, "Making progress visible", "A handful of KPIs per dimension, reviewed monthly (baselines to be measured in discovery)");
  const kpis = [["FaDesktop", "Fiori adoption", "% active users on Fiori", "0% → 75%"],
    ["FaUsers", "Work Zone reach", "Users with a role-based site", "0 → 600"],
    ["FaProjectDiagram", "Integration", "% interfaces on Integration Suite", "5% → 70%"],
    ["FaCode", "Clean core", "ATC level C/D findings", "↓ 50%"],
    ["FaDatabase", "Data quality", "DQ rule pass rate", "72% → 95%"],
    ["FaTable", "Custom fields", "Z-fields mapped or exposed", "0% → 90%"],
    ["FaSyncAlt", "Flow", "Median lead time (days)", "45 → 20"],
    ["FaServer", "Release currency", "Months behind latest FPS", "12 → 3"]];
  kpis.forEach(([ic, h, d, v], i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = 0.6 + col * 3.1, y = 1.85 + row * 1.75, w = 2.9;
    card(s, x, y, w, 1.55);
    circle(s, ic, x + 0.2, y + 0.2, 0.55);
    T(s, h, x + 0.9, y + 0.2, w - 1.0, 0.55, { fontSize: 14, bold: true, color: C.dark, valign: "middle" });
    T(s, v, x + 0.2, y + 0.8, w - 0.4, 0.4, { fontFace: HF, fontSize: 20, bold: true, color: C.teal });
    T(s, d, x + 0.2, y + 1.18, w - 0.4, 0.3, { fontSize: 11, color: C.muted });
  });
  card(s, 0.6, 5.5, 12.1, 1.35, C.tint, false);
  T(s, "Show, don’t tell", 0.85, 5.6, 3, 0.4, { fontSize: 15, bold: true, color: C.teal });
  T(s, bullets([
    [["Board: "], "Kanban/sprint board visible to business (Cloud ALM or existing tool)."],
    [["Demo: "], "every two weeks, users see working Fiori apps, sites and fixes."],
  ]), 0.85, 6.0, 5.6, 0.8, { fontSize: 12.5 });
  T(s, bullets([
    [["Trends: "], "tech-debt interest, C/D findings and flow distribution over time."],
    [["Wins: "], "one-page monthly note — what shipped, what it saved, what’s next."],
  ]), 6.6, 6.0, 5.9, 0.8, { fontSize: 12.5 });
  footer(s, n);
  s.addNotes("Targets shown are to Q4-2027 and are placeholders to be set once baselines are measured. The Planner's KPI Dashboard computes live backlog counts and health signals (stale items, open C/D items, annual interest cost of open debt) and a RAG status against targets.");

  // ---------------------------------------------------------------- 13 Roadmap
  s = pres.addSlide(); n++;
  title(s, "Roadmap: 15 months, six workstreams", "Foundations first, then scale; dates are proposals");
  const qx0 = 2.9, qw = 1.95, qlabels = ["Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"];
  qlabels.forEach((ql, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: qx0 + i * qw, y: 1.8, w: qw - 0.04, h: 0.4, fill: { color: i % 2 ? C.grey : "E5E7EB" }, line: { color: C.white } });
    T(s, ql, qx0 + i * qw, 1.8, qw, 0.4, { fontSize: 12, bold: true, color: C.dark, align: "center", valign: "middle" });
  });
  const phases = [["Mobilise & baseline", 0, 0.8, C.slate], ["Foundations & quick wins", 0.8, 2.0, C.teal], ["Scale", 2.0, 4.0, C.teal2], ["Optimise & innovate", 3.3, 5.0, C.amber]];
  phases.forEach(([p, a, b, col], i) => {
    const y = 2.28 + (i === 3 ? 0.36 : 0);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: qx0 + a * qw, y, w: (b - a) * qw - 0.05, h: 0.32, rectRadius: 0.06, fill: { color: col }, line: { color: col } });
    T(s, p, qx0 + a * qw, y, (b - a) * qw - 0.05, 0.32, { fontSize: 11, bold: true, color: C.white, align: "center", valign: "middle" });
  });
  const lanes = [
    ["UX / Fiori", C.teal, [["Fiori foundation", 0.2, 1.3, 0], ["Finance wave", 0.7, 2.0, 1], ["Supply chain wave", 2.0, 3.3, 0], ["Sales / QM / PM", 3.0, 4.7, 1]]],
    ["Work Zone", "0D9488", [["Subaccount, IdP", 0.35, 1.3, 0], ["Pilot + plant supervisor site", 1.35, 3.0, 0]]],
    ["Integration", C.brown, [["Landing zone", 0.2, 1.2, 0], ["Inventory, ISA-M", 0.35, 1.35, 1], ["Migration waves 1\u20133", 1.35, 4.9, 0]]],
    ["Data", C.purple, [["Z-field inventory", 0.2, 1.3, 0], ["DQ rules + BP clean-up", 0.7, 3.0, 1], ["MDG decision & start", 3.0, 4.9, 1]]],
    ["Clean core", C.red, [["Retire unused code", 0.7, 2.0, 0], ["Remediate C/D; ABAP Cloud for all new", 2.0, 4.9, 0]]],
    ["Platform / ops", C.blue, [["Cloud ALM set-up", 0.2, 2.0, 0], ["Test automation", 1.0, 3.0, 1], ["Release / FPS upgrade", 3.0, 4.3, 0]]],
  ];
  lanes.forEach(([name, col, bars], i) => {
    const y = 3.15 + i * 0.63;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: y - 0.04, w: 12.1, h: 0.6, fill: { color: i % 2 ? C.white : "F8FAFC" }, line: { color: "F1F5F9" } });
    T(s, name, 0.7, y, 2.1, 0.52, { fontSize: 13, bold: true, color: C.dark, valign: "middle" });
    const two = bars.some(bb => bb[3] === 1);
    bars.forEach(([lbl, a, b, r]) => {
      const bh = 0.24, by = two ? y + r * 0.28 : y + 0.14;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: qx0 + a * qw, y: by, w: (b - a) * qw - 0.05, h: bh, rectRadius: 0.05, fill: { color: col }, line: { color: col } });
      T(s, lbl, qx0 + a * qw + 0.06, by, (b - a) * qw - 0.15, bh, { fontSize: 9.5, bold: true, color: C.white, valign: "middle" });
    });
  });
  footer(s, n);
  s.addNotes("Phase 0 (Oct-Nov 2026): mobilise governance and baseline with SAP tools. Phase 1 (to ~Feb 2027): Fiori foundation and first finance wave, Work Zone and Integration Suite landing zones, custom-field inventory, Cloud ALM. Phase 2 (2027): scale Fiori by role, migrate interfaces in waves, data quality programme, remediate C/D code. Phase 3 (H2 2027): release upgrade, AI/Joule readiness, process automation. Full activity-level Gantt is in the Planner's Roadmap tab.");

  // ---------------------------------------------------------------- 14 Workstream plays
  s = pres.addSlide(); n++;
  title(s, "Three plays for the biggest gaps", "Each play starts with SAP standard and builds only what standard can’t do");
  const plays = [
    ["FaDesktop", "Fiori & Work Zone", ["Pull 12 months of transaction usage; get app recommendations (Pathfinder / Fiori Apps Library)", "Design roles as spaces & pages per job, not per module", "Roll out in business waves with key users as champions", "Work Zone standard as the single entry point: Fiori, BTP apps and non-SAP links", "Measure adoption; retire GUI transactions as apps land"]],
    ["FaProjectDiagram", "Integration Suite", ["Landing zone: naming, packages, security, cTMS transports, alerting via Cloud ALM", "Inventory every interface; classify with ISA-M", "Prefer standard APIs and events from SAP Business Accelerator Hub", "Migrate in waves: highest-failure and PI/PO interfaces first", "Stop new point-to-point builds via design authority"]],
    ["FaTable", "Data & custom fields", ["Inventory every business-data Z-field (use the 8-question checklist)", "Map to standard where S/4 now has a home; else re-create with Custom Fields app", "Assign data owners; define DQ rules and a monthly score", "Clean duplicates (business partner, material) before migrating fields", "Decide on MDG / governance tooling with a business case"]],
  ];
  plays.forEach(([ic, h, items], i) => {
    const x = 0.6 + i * 4.1, w = 3.9;
    card(s, x, 1.85, w, 5.0);
    circle(s, ic, x + 0.25, 2.05, 0.7);
    T(s, h, x + 1.1, 2.05, w - 1.2, 0.7, { fontSize: 18, bold: true, color: C.dark, valign: "middle" });
    T(s, items.map((t, k) => ({ text: t, options: { bullet: { type: "number" }, breakLine: k < items.length - 1 } })), x + 0.25, 2.95, w - 0.45, 3.8, { fontSize: 14, paraSpaceAfter: 10 });
  });
  footer(s, n);
  s.addNotes("Custom fields are the linchpin: while business data sits in SE11 appends, standard Fiori apps, OData APIs, Work Zone content and analytics cannot use it. Fixing that unlocks the Fiori and Work Zone plays. Integration Suite standards must be in place before volume grows, or the new platform becomes the next generation of debt.");

  // ---------------------------------------------------------------- 15 First 90 days
  s = pres.addSlide(); n++;
  title(s, "The first 90 days", "Visible early wins while the baseline is built");
  const d90 = [["Days 1–30", "Mobilise", ["Name product owner, EA, design authority", "Choose backlog tool (Cloud ALM or existing)", "Load the Planner register; run first triage", "Run Readiness Check, Pathfinder, ATC clean-core, SCMON", "Start interface and Z-field inventories"]],
    ["Days 31–60", "Baseline & foundations", ["Score and rank top 50 items with WSJF", "Agree capacity guardrails and budget cap", "Fiori launchpad foundation + first finance roles", "Work Zone subaccount, IdP; Integration Suite landing zone", "First KPI dashboard to leadership"]],
    ["Days 61–90", "First wins", ["First Fiori apps live for finance users", "Pilot Work Zone site demoed", "Top 3 failing interfaces fixed or migrated", "First Z-fields mapped / exposed; DQ score published", "Quarterly roadmap refresh with business"]]];
  d90.forEach(([p, h, items], i) => {
    const x = 0.6 + i * 4.1, w = 3.9;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.85, w, h: 0.95, rectRadius: 0.08, fill: { color: [C.dark, C.teal, C.teal2][i] }, line: { color: [C.dark, C.teal, C.teal2][i] } });
    T(s, p, x + 0.25, 1.9, w - 0.5, 0.4, { fontSize: 13, bold: true, color: "CCFBF1" });
    T(s, h, x + 0.25, 2.28, w - 0.5, 0.45, { fontSize: 19, bold: true, color: C.white });
    card(s, x, 2.95, w, 3.9);
    T(s, bullets(items), x + 0.25, 3.15, w - 0.45, 3.6, { fontSize: 15, paraSpaceAfter: 12 });
  });
  footer(s, n);
  s.addNotes("The 90-day plan is designed so users see something new by day 90 (Fiori apps, a Work Zone pilot, fewer interface failures), which builds support for the longer clean-core work.");

  // ---------------------------------------------------------------- 16 Questions
  s = pres.addSlide(); n++;
  title(s, "Questions we need answered to finalise the plan", "Please bring answers (or owners) to the next session");
  const qsets = [
    ["Landscape & licensing", ["S/4HANA deployment (RISE private, on-premise, public) and current release / FPS?", "BTP contract model and entitlements (Work Zone edition, Integration Suite, credits)?", "Is PI/PO in the landscape, and until when?"]],
    ["Budget & team", ["Current IT/AMS run budget and team size; what is fixed vs flexible?", "Is the partner contract ticket-based or capacity-based?", "Who can approve capacity shifts between work types?"]],
    ["Backlog & tools", ["Where do requests and incidents live today (ServiceNow, Jira, Excel, Cloud ALM)?", "Is SAP Cloud ALM activated, and which apps are in use?", "Is there an existing design authority / architecture board?"]],
    ["UX & Work Zone", ["Fiori front-end: embedded or hub? Any roles built at go-live?", "Which user groups want Work Zone first, and for what?", "Any non-SAP apps that must appear on the launchpad?"]],
    ["Data & custom fields", ["How many business-data Z-fields, in which objects?", "Which data domains hurt most, and who owns them?", "Is MDG or another governance tool licensed or planned?"]],
    ["Outcomes", ["Top 3 business outcomes leadership expects in 12 months?", "Any hard dates (audits, acquisitions, plant roll-outs, maintenance ends)?", "Appetite for AI / Joule use cases in 2027?"]],
  ];
  qsets.forEach(([h, items], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.1, y = 1.8 + row * 2.6, w = 3.9;
    card(s, x, y, w, 2.45);
    circle(s, "FaQuestion", x + 0.2, y + 0.15, 0.5, i % 2 ? C.teal : C.dark);
    T(s, h, x + 0.85, y + 0.15, w - 1, 0.5, { fontSize: 15, bold: true, color: C.dark, valign: "middle" });
    T(s, bullets(items), x + 0.2, y + 0.75, w - 0.35, 1.65, { fontSize: 12, paraSpaceAfter: 5 });
  });
  footer(s, n);
  s.addNotes("These questions change the plan materially: deployment model and BTP entitlements decide tooling and cost; budget model decides how capacity allocation is enforced; custom field volume sizes the data workstream. The Quick Reference Guide has the full interview question bank by role.");

  // ---------------------------------------------------------------- 17 Decisions & next steps
  s = pres.addSlide(); n++;
  s.background = { color: C.dark };
  T(s, "Decisions requested", 0.8, 0.6, 6, 0.7, { fontFace: HF, fontSize: 32, bold: true, color: C.white });
  const dec = ["Adopt one backlog for all five work types, with the register as the single source", "Approve capacity guardrails (starting ~45% tech debt + enablers) within the current budget", "Name a product owner, business owners per dimension, and a design authority", "Choose the backlog tool: SAP Cloud ALM or the existing enterprise tool", "Start the 30-day discovery using SAP’s free tools"];
  dec.forEach((d, i) => {
    const y = 1.55 + i * 0.95;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.6, h: 0.6, fill: { color: C.teal }, line: { color: C.teal } });
    T(s, String(i + 1), 0.8, y, 0.6, 0.6, { fontFace: HF, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, d, 1.65, y - 0.05, 5.8, 0.75, { fontSize: 15, color: "E2E8F0", valign: "middle" });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.0, y: 0.6, w: 4.6, h: 6.2, rectRadius: 0.1, fill: { color: "1F4550" }, line: { color: "1F4550" } });
  T(s, "Next steps", 8.3, 0.85, 4, 0.5, { fontSize: 20, bold: true, color: C.teal2 });
  T(s, bullets([
    "Share Quick Reference Guide with leads; run role interviews (2 weeks)",
    "Load findings into the Planner register; first triage",
    "Run SAP discovery tools; baseline KPIs",
    "Scoring workshop: WSJF top 50",
    "Portfolio review: confirm guardrails, roadmap and 90-day plan",
  ], { color: "E2E8F0" }), 8.3, 1.5, 4.05, 4.3, { fontSize: 14, color: "E2E8F0", paraSpaceAfter: 12 });
  T(s, "Companion files: Planner (.xlsx) and Quick Reference Guide (.docx)", 8.3, 6.0, 4.05, 0.6, { fontSize: 11, italic: true, color: "94A3B8" });
  s.addNotes("Close by asking for the five decisions. The first four are organisational and cost nothing; the fifth starts discovery using tools included in existing SAP contracts.");

  await pres.writeFile({ fileName: OUT });
  console.log("wrote", OUT);
})();
