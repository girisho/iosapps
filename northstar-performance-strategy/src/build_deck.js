// NorthStar Performance Assurance Strategy deck (International Motors brand).
const pptxgen = require("pptxgenjs");
const path = require("path");
const B = require(path.join(process.env.SKILL_DIR, "scripts", "brand.js"));
const { COLORS: C, FONTS: F, BADGE_SEQUENCE } = B;

const OUT = process.argv[2] || "deck.pptx";
const PNG = (n) => path.join(__dirname, "png", n);

const pres = B.newDeck(pptxgen, "NorthStar Performance Assurance Strategy");
let page = 1;

function content(title, subtitle, opts = {}) {
  const s = pres.addSlide();
  page += 1;
  B.addContentChrome(s, { title, subtitle, pageNum: page, titleSize: opts.titleSize || 26 });
  return s;
}

function txt(s, t, o) {
  s.addText(t, Object.assign({ isTextBox: true, margin: 0, fontFace: F.BODY, color: C.CHARCOAL, valign: "top" }, o));
}

function bullets(items, size = 12.5, color = C.BODY_SLATE) {
  return items.map((t, i) => ({
    text: t,
    options: { bullet: { indent: 14 }, fontSize: size, color, breakLine: i < items.length - 1, paraSpaceAfter: 5 },
  }));
}

function card(s, x, y, w, h, fill = C.CARD_GRAY) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill } });
}

function chip(s, x, y, w, h, label, fill, size = 12, color = C.WHITE) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color: fill } });
  txt(s, label, { x, y, w, h, fontSize: size, bold: true, color, align: "center", valign: "middle" });
}

function badge(s, x, y, d, n, fill, size = 14) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
  txt(s, String(n), { x, y, w: d, h: d, fontSize: size, bold: true, color: C.WHITE, align: "center", valign: "middle" });
}

function table(s, header, body, o) {
  const rows = B.brandTableRows(header, body, o.fontSize || 11);
  s.addTable(rows, {
    x: o.x ?? 0.556, y: o.y ?? 1.55, w: o.w ?? 12.222, colW: o.colW,
    rowH: o.rowH || 0.3, border: { type: "solid", pt: 0.5, color: "D5D8DC" }, margin: [3, 6, 3, 6],
    autoPage: false,
  });
}

// ------------------------------------------------------------------ 1 Cover
{
  const s = pres.addSlide();
  B.addCoverChrome(s, {
    title: "Performance assurance strategy",
    subtitle: "Proving S/4HANA, BTP and Central Finance at production load before go-live\n\nProject NorthStar  |  October 2026  |  Draft for VP IT and program leadership",
  });
}

// ------------------------------------------------------------------ 2 Executive summary
{
  const s = content("Executive summary", "A ring-fenced, risk-based workstream can still prove the solution at load before Dec 15, if we decide by Oct 9");
  const cols = [
    ["THE SITUATION", C.STEEL, [
      "No plan, owner, budget or team for performance testing, while Mock-2 and SIT2 are distressed",
      "10 weeks to tech go-live on Dec 15. UAT Oct 26 to Nov 20, cutover from Nov 23",
      "Pre-prod is about 50% of PRD. Volumes and peak profiles are not yet known",
      "Risk concentrates in the CFIN JE feed and trial balance match, VSM truck orders, billing with OneSource and DRC Mexico, VIM, and 168 BTP interfaces",
    ]],
    ["OUR ANSWER", C.CHARCOAL, [
      "Run performance assurance as its own workstream with a named owner and a dedicated team, separate from SIT2 and Mock staff",
      "Risk-tiered scope: about 35 scripted end-to-end scenarios instead of several hundred bespoke tests",
      "Start shift-left baselining in SIT2 this week. Most go-live performance defects are code, not hardware",
      "Execute in a protected pre-prod window Nov 2 to Dec 4 and translate results with a three-class scaling model",
    ]],
    ["WHAT WE NEED BY OCT 9", C.ORANGE, [
      "Approve the workstream, the owner and the PwC change request",
      "Fund a specialist performance team of about 6 people for 10 weeks",
      "Reserve pre-prod Nov 2 to Dec 4 for performance cycles",
      "Legacy and SaaS owners commit test capacity or accept stubs by Oct 16",
      "Adopt the KPIs as a formal gate on Dec 4, feeding tech go-live readiness",
    ]],
  ];
  cols.forEach(([h, col, items], i) => {
    const x = 0.556 + i * 4.13;
    chip(s, x, 1.6, 3.95, 0.5, h, col, 13, col === C.ORANGE ? C.CHARCOAL : C.WHITE);
    card(s, x, 2.18, 3.95, 4.0);
    txt(s, bullets(items, 12.5), { x: x + 0.18, y: 2.35, w: 3.6, h: 4.3 });
  });
}

// ------------------------------------------------------------------ 3 Timeline
{
  const s = content("Ten weeks to tech go-live", "Execution runs in parallel to UAT in a protected pre-prod window, ending with a performance gate on Dec 4");
  s.addImage({ path: PNG("02-timeline-deck.png"), x: 0.556, y: 1.5, w: 12.222, h: 12.222 * 720 / 1730 });
  txt(s, "The cutover rehearsal from Nov 23 overlaps the retest window. Pre-prod sequencing must be decided now, not discovered in November.", {
    x: 0.556, y: 6.62, w: 12.2, h: 0.3, fontSize: 12, bold: true, color: C.MAROON,
  });
}

// ------------------------------------------------------------------ 4 Seven requirements
{
  const s = content("The seven requirements, answered", "Each requirement from the Oct 1 call has a concrete response, an owner and a ready-by date");
  table(s, ["#", "Requirement raised", "Our response", "Owner", "Ready by"], [
    ["1", "Specific tests for apps, integrations and batch", "Risk-tiered catalog: about 35 Tier 1 scripted scenarios, about 70 Tier 2 component checks, telemetry for the rest. AI-assisted triage of the 168 interfaces, RICEFW list and Control-M export", "INTL perf lead, PwC", "Oct 16"],
    ["2", "KPIs for each test", "Standard KPI library by metric class, thresholds tuned per Tier 1 scenario and signed by process owners", "PwC perf manager, process owners", "Oct 23"],
    ["3", "Environment to test in", "Pre-prod (50% of PRD) with full Mock data volumes, protected Nov 2 to Dec 4. ECS refresh, config parity and snapshot restore points", "Basis, SAP ECS", "Oct 30"],
    ["4", "Tooling over the environment", "Keep NeoLoad. Add SAP-native ABAP and HANA analysis, Integration Suite monitoring, Cloud ALM and service virtualization stubs", "Perf engineering", "Oct 23"],
    ["5", "Tests loaded with data and volumes", "Workload model from legacy volumes, synthetic data factory, scripts parameterized for sequential and concurrent runs", "Perf engineering, test data", "Nov 2"],
    ["6", "Near-production roles and integration security", "Performance users cloned from production business roles, communication users with production-like authorizations, no SAP_ALL", "Security and GRC", "Oct 30"],
    ["7", "Environment scaling estimates", "ECS configuration sheet for pre-prod and PRD, a three-class scaling model, and a calibration run before cycle 1", "Basis, INTL perf lead", "Nov 3"],
  ], { y: 1.55, colW: [0.4, 2.6, 6.322, 1.95, 0.95], fontSize: 11, rowH: 0.66 });
}

// ------------------------------------------------------------------ 5 Heat map
{
  const s = content("Where the performance risk lives", "Working hypothesis until volumes are mined in week 1. Ratings drive the Tier 1 selection");
  const H = { VH: ["Very high", C.MAROON, C.WHITE], H: ["High", C.ORANGE, C.CHARCOAL], M: ["Medium", C.CARD_GRAY, C.CHARCOAL], L: ["Low", "F4F5F6", C.MUTED_GRAY] };
  const data = [
    ["CFIN JE feed (Infor LN, DataStage, JDBC) and TB match", "H", "H", "VH", "H", "VH", "Month-end JE volume must post and reconcile inside the close calendar"],
    ["OTC truck order (VSM / AVC, pricing, OneSource)", "M", "VH", "VH", "H", "VH", "Complex configuration plus a synchronous tax call on every save"],
    ["Billing, invoice outbound, DRC Mexico CFDI", "H", "H", "VH", "H", "VH", "Revenue and regulatory deadline. Chain of tax, forms, DRC and legacy"],
    ["VIM vendor invoices (OCR, workflow, posting)", "H", "H", "H", "VH", "H", "Already a known pain point. Workflow and background job load"],
    ["BTP Integration Suite (168 interfaces)", "H", "M", "H", "H", "H", "Shared choke points: tenant limits, JMS, EOIO, Cloud Connector"],
    ["Batch: Control-M, SOA, DataStage", "H", "H", "H", "M", "H", "Nightly and month-end windows across US and Mexico time zones"],
    ["Warranty claims via Pega", "M", "M", "H", "H", "H", "Burst inbound claims, credit memo postings"],
    ["Financial close and analytics", "M", "M", "VH", "M", "H", "Heavy ACDOCA reads during the first close"],
    ["Ariba indirect procurement", "M", "L", "M", "L", "M", "Standard integration, moderate volume"],
    ["Fiori launchpad, login, roles", "M", "L", "M", "M", "M", "Morning login storm, large role catalogs"],
  ];
  const rows = [["Value stream", "Volume", "Complexity", "Business impact", "Novelty / known issues", "Overall", "Why"].map(t => ({ text: t, options: { fill: { color: C.CHARCOAL }, color: C.WHITE, bold: true, fontSize: 11, fontFace: F.BODY, valign: "middle" } }))];
  data.forEach((r) => {
    rows.push(r.map((v, j) => {
      if (j >= 1 && j <= 5) {
        const [lab, fill, col] = H[v];
        return { text: lab, options: { fill: { color: fill }, color: col, bold: j === 5, fontSize: 10.5, fontFace: F.BODY, align: "center", valign: "middle" } };
      }
      return { text: v, options: { fill: { color: C.WHITE }, color: C.CHARCOAL, bold: j === 0, fontSize: 10.5, fontFace: F.BODY, valign: "middle" } };
    }));
  });
  s.addTable(rows, { x: 0.556, y: 1.55, w: 12.222, colW: [3.3, 0.9, 1.0, 1.1, 1.2, 0.95, 3.772], rowH: 0.46, border: { type: "solid", pt: 0.75, color: C.WHITE }, margin: [3, 6, 3, 6] });
}

// ------------------------------------------------------------------ 6 Pyramid
{
  const s = content("Risk-tiered scope", "Test deeply where the risk is. Watch everything else with telemetry");
  const h = 3.95, w = h * 1600 / 590;
  s.addImage({ path: PNG("03-risk-tier-pyramid-deck.png"), x: (13.3333 - w) / 2, y: 1.5, w, h });
  B.addNote(s, "How it works:  every object in the interface list, RICEFW list, Fiori and T-code usage list and Control-M export gets a risk score. Tier 1 is scripted and load tested, Tier 2 gets volume injection without UI scripting, and Tier 3 is watched in SIT2 and UAT telemetry. This answers \"several hundred tests\" with defensible coverage instead of brute force.");
}

// ------------------------------------------------------------------ 7 Tier 1 set
{
  const s = content("The Tier 1 scenario set: 35 end-to-end flows", "Draft for the Oct 15 sign-off workshop. Full catalog with KPIs and scores is in the workbook");
  const groups = [
    ["Order to cash and billing", 8, C.MAROON, ["VSM truck order: configure, price, tax, save", "Order change and reconfiguration", "Inbound dealer and legacy orders via API", "Delivery and goods issue", "Billing run with OneSource and output", "Invoice outbound to legacy apps", "DRC Mexico CFDI to PAC and status back", "Cash application and customer payments"]],
    ["Central Finance and close", 7, C.INTL_BLUE, ["Infor LN JE feed at month-end peak", "AIF error reprocessing at volume", "Trial balance match S/4 versus legacy", "FX revaluation, depreciation, accruals", "Financial statements and analytical apps", "GL extracts to legacy and reporting", "Period open and close steps"]],
    ["P2P and VIM", 6, C.STEEL, ["Ariba PO replication to S/4", "Goods receipt and service entry", "VIM OCR intake in bulk", "VIM approval workflow, concurrent users", "Invoice posting and 3-way match", "Payment run and bank file"]],
    ["Warranty", 3, C.STEEL, ["Pega claim inbound burst", "Claim adjudication and credit memo batch", "Claim status back to Pega"]],
    ["Integration and batch", 6, C.CHARCOAL, ["Top 20 iFlow mix at design peak", "OneSource latency under concurrent load", "Endpoint outage and backlog drain", "Nightly Control-M critical path", "Month-end batch chain", "DataStage and SOA jobs alongside online"]],
    ["Platform and mixed load", 5, C.CHARCOAL, ["Morning login storm and launchpad", "Integrated peak hour, all streams", "Eight-hour soak", "Stress to break point", "Top heavy reports and CDS views"]],
  ];
  groups.forEach(([h, n, col, items], i) => {
    const cx = i % 3, cy = Math.floor(i / 3);
    const x = 0.556 + cx * 4.13, y = 1.55 + cy * 2.68;
    card(s, x, y, 3.95, 2.55);
    chip(s, x, y, 3.95, 0.42, `${h}  (${n})`, col, 12.5);
    txt(s, bullets(items, 11, C.BODY_SLATE).map(b => { b.options.paraSpaceAfter = 2; return b; }), { x: x + 0.15, y: y + 0.52, w: 3.7, h: 1.98 });
  });
}

// ------------------------------------------------------------------ 8 Architecture
{
  const s = content("Test architecture and injection points", "Four injection points, one measurement clock across S/4HANA, BTP, DataStage and the legacy endpoints");
  const h = 5.4, w = h * 1600 / 920;
  s.addImage({ path: PNG("01-test-architecture-deck.png"), x: (13.3333 - w) / 2, y: 1.48, w, h });
}

// ------------------------------------------------------------------ 9 Environment strategy
{
  const s = content("Environment strategy", "Pre-prod is the primary stage. Two fallbacks protect the gate if pre-prod time or capacity runs out");
  const opts = [
    ["A", "RECOMMENDED", "Protected pre-prod window", "Nov 2 to Dec 4 reserved for performance cycles. Shared with cutover rehearsal by agreed slots, nights and weekends", C.CHARCOAL],
    ["B", "ADD-ON", "ECS temporary app-tier upsize", "Ask ECS to quote extra application servers for one cycle. Confirms class B scaling and narrows the forecast error", C.INTL_BLUE],
    ["C", "CONTINGENCY", "PRD window before cutover", "Only if pre-prod results are inconclusive. Full-size hardware, then snapshot restore. Needs ECS and cutover lead agreement", C.MAROON],
  ];
  opts.forEach(([k, tag, h, body, col], i) => {
    const y = 1.6 + i * 1.72;
    card(s, 0.556, y, 6.6, 1.55);
    badge(s, 0.75, y + 0.2, 0.5, k, col, 16);
    txt(s, tag, { x: 1.4, y: y + 0.17, w: 5.5, h: 0.25, fontSize: 10.5, bold: true, color: C.MUTED_GRAY });
    txt(s, h, { x: 1.4, y: y + 0.42, w: 5.6, h: 0.32, fontSize: 15, bold: true });
    txt(s, body, { x: 1.4, y: y + 0.78, w: 5.6, h: 0.7, fontSize: 12, color: C.BODY_SLATE });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.45, y: 1.6, w: 5.33, h: 5.0, rectRadius: 0.08, fill: { color: C.NOTE_FILL }, line: { color: C.NOTE_BORDER, width: 0.75 } });
  txt(s, "READY-TO-TEST CHECKLIST", { x: 7.65, y: 1.75, w: 5.0, h: 0.3, fontSize: 13, bold: true });
  txt(s, bullets([
    "Full Mock data volumes, with table sizes checked against PRD projection",
    "Transport and configuration parity with PRD",
    "HANA parameters, work processes and number range buffering match PRD",
    "Integration Suite test tenant and Cloud Connector set up like PRD",
    "Performance users and roles cloned from production business roles",
    "Stubs live for endpoints that cannot take load",
    "Snapshot taken before each cycle, restore tested",
    "Monitoring retention extended (ST03N, STAD, SQLM, IS logs)",
    "ECS configuration sheet for pre-prod and PRD on file",
  ], 11.5), { x: 7.65, y: 2.15, w: 4.95, h: 4.35 });
}

// ------------------------------------------------------------------ 10 Scaling
{
  const s = content("Reading results from a 50% pre-prod", "Not every metric doubles in production. Three classes, three translation rules");
  const h = 5.3, w = h * 1600 / 720;
  s.addImage({ path: PNG("04-scaling-model-deck.png"), x: (13.3333 - w) / 2, y: 1.5, w, h });
}

// ------------------------------------------------------------------ 11 Tooling
{
  const s = content("Tooling: keep NeoLoad, complete the stack", "Switching load tools now would cost 3 to 4 weeks we do not have. The gaps are in monitoring, stubs and analysis");
  table(s, ["Layer", "Tool", "What it does for us"], [
    ["Load injection, UI", "NeoLoad (licensed)", "Fiori and OData, SAP GUI and web protocols. All Tier 1 user scripts"],
    ["Load injection, non-UI", "NeoLoad API tests or JMeter, DataStage replay jobs", "iFlow payloads, JDBC JE volumes, file drops at design rate"],
    ["Service virtualization", "Mock iFlows on the BTP test tenant, or WireMock", "Stand in for PAC, OneSource and legacy endpoints that cannot take load"],
    ["ABAP and HANA analysis", "ST03N, STAD, SQLM, SAT, ST05, HANA Cockpit, SQL plan cache", "Find the expensive statement, the hot code path, the lock"],
    ["Integration monitoring", "Integration Suite monitor, JMS queues, Cloud Connector, AIF, eDocument Cockpit", "Throughput, backlog, retries and error rates per interface"],
    ["Observability and hypercare", "SAP Cloud ALM or Focused Run, existing APM if licensed", "Same dashboards and thresholds carry into hypercare"],
    ["Results intelligence", "AI-assisted analysis over exported metrics", "Anomaly detection, triage to code owners, daily readout"],
  ], { y: 1.55, colW: [2.3, 4.4, 5.522], fontSize: 11.5, rowH: 0.48 });
  B.addNote(s, "Recommendation:  keep NeoLoad for this go-live. It is licensed and covers the SAP protocols we need. Revisit the tool choice after hypercare, when the question becomes continuous performance regression for future releases rather than a ten-week sprint.");
}

// ------------------------------------------------------------------ 12 Workload model and data
{
  const s = content("Workload model and test data", "Peak is defined from evidence, not opinion. Data is production-shaped, not empty-system clean");
  B.addProcessCard(s, 0, "Mine volumes", "Infor LN JE counts, legacy orders and invoices, Ariba, Pega, Control-M history");
  B.addProcessCard(s, 1, "Find the peak", "Busiest hour of the busiest day: month-end days 1 to 3, billing cut-off, dealer order peaks");
  B.addProcessCard(s, 2, "Add headroom", "Design load = 1.5 x measured peak hour, plus 2027 growth");
  B.addProcessCard(s, 3, "Build the mix", "Little's Law turns hourly volume into virtual users and pacing per scenario");
  B.addNote(s, "Test data:  master data comes from the Mock-converted load so table sizes are realistic. Transactions are synthesized: balanced JEs that pass CFIN mapping, valid VSM configurations, CFDI-valid Mexican invoices, invoice images for VIM OCR, warranty claims. A pre-prod snapshot before each cycle lets us reset in hours, not days.");
}

// ------------------------------------------------------------------ 13 KPIs and gate
{
  const s = content("KPIs and the Dec 4 go / no-go gate", "Proposed defaults. Process owners confirm thresholds per Tier 1 scenario by Oct 23");
  table(s, ["Class", "KPI", "Proposed threshold"], [
    ["Online, simple", "Fiori or GUI step response, 90th percentile", "2 seconds or less"],
    ["Online, complex", "VSM configure, price and save; VIM approval", "5 seconds or less"],
    ["Synchronous API", "OneSource tax call, 95th percentile", "800 ms or less, no timeouts"],
    ["Async interfaces", "Sustained throughput versus design peak", "1.5 x peak, no backlog growth"],
    ["Resilience", "Backlog drain after a 1-hour endpoint outage", "60 minutes or less, zero loss"],
    ["Central Finance", "JE lines posted per hour; TB match", "1.5 x month-end peak; 100% match"],
    ["Batch", "Critical path versus batch window", "Fits with 20% buffer"],
    ["Platform", "CPU, HANA memory, free dialog work processes", "70% / 80% / 20% free at PRD-equivalent"],
    ["Endurance", "Degradation over 8 hours", "Under 10%, no memory growth"],
  ], { x: 0.556, y: 1.55, w: 7.6, colW: [1.6, 3.4, 2.6], fontSize: 11, rowH: 0.47 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.45, y: 1.55, w: 4.33, h: 5.17, rectRadius: 0.08, fill: { color: C.CHARCOAL }, line: { color: C.CHARCOAL } });
  txt(s, "GO / NO-GO ON DEC 4", { x: 8.7, y: 1.75, w: 3.9, h: 0.3, fontSize: 14, bold: true, color: C.ORANGE });
  txt(s, bullets([
    "All severity 1 performance defects closed",
    "At least 90% of Tier 1 scenarios meet KPI; the rest have a signed workaround and a hypercare monitor",
    "Month-end CFIN volume posted and trial balance matched inside the close calendar",
    "Batch critical path fits the window",
    "No class C limit reached at full design load",
    "Scaling forecast for PRD documented and accepted",
  ], 12, C.WHITE), { x: 8.7, y: 2.2, w: 3.9, h: 4.4 });
}

// ------------------------------------------------------------------ 14 AI
{
  const s = content("Where intelligence accelerates the work", "AI shortens the slowest manual steps. People still own every decision and every sign-off");
  const items = [
    ["Inventory triage", "Read FSDs, the interface list, RICEFW and the Control-M export. Draft classification and risk scores for a two-hour validation workshop", "Weeks to days"],
    ["Workload mining", "Parse legacy GL counts, SOA and DataStage logs, and job history to find peak hours and arrival patterns", "Peak from evidence"],
    ["Synthetic data factory", "Generate balanced JEs, valid VSM configurations, CFDI-valid invoices, VIM invoice images and warranty claims", "Volume without PII"],
    ["Script acceleration", "Draft API payloads from iFlow and OpenAPI specs, and suggest correlation and parameterization for NeoLoad scripts", "Faster Tier 1 build"],
    ["Results triage", "Flag anomalies across ST03N, HANA and Integration Suite metrics, and route the expensive statement to its code owner", "Hours to root cause"],
    ["Daily readout", "Auto-draft the daily executive status from test results and the defect log, reviewed by the performance lead", "Leaders stay informed"],
  ];
  items.forEach(([h, body, gain], i) => {
    const cx = i % 3, cy = Math.floor(i / 3);
    const x = 0.556 + cx * 4.13, y = 1.55 + cy * 2.35;
    card(s, x, y, 3.95, 2.2);
    badge(s, x + 0.18, y + 0.18, 0.44, i + 1, BADGE_SEQUENCE[i % 4], 14);
    txt(s, h, { x: x + 0.75, y: y + 0.22, w: 3.1, h: 0.36, fontSize: 14.5, bold: true, valign: "middle" });
    txt(s, body, { x: x + 0.2, y: y + 0.75, w: 3.6, h: 1.0, fontSize: 11.5, color: C.BODY_SLATE });
    txt(s, gain, { x: x + 0.2, y: y + 1.78, w: 3.6, h: 0.3, fontSize: 11.5, bold: true, color: C.ORANGE });
  });
  txt(s, "Also use what we already pay for: SAP Enterprise Support Going-Live Check (confirm entitlement), an ECS sizing review, and SAP Cloud ALM.", {
    x: 0.556, y: 6.32, w: 12.2, h: 0.35, fontSize: 12, bold: true, color: C.CHARCOAL,
  });
}

// ------------------------------------------------------------------ 15 First 10 days
{
  const s = content("Start this week: the first ten days", "None of these steps needs the test environment. All of them shorten the path to Nov 2");
  const steps = [
    ["Name the owner", "International performance lead and PwC counterpart", "Oct 5"],
    ["Turn on telemetry in SIT2", "ST03N and STAD retention, SQLM, HANA expensive statements, IS trace", "Oct 5 to 9"],
    ["Open ECS tickets", "Pre-prod and PRD config sheet, refresh plan, snapshots, upsize quote", "Oct 5"],
    ["Request Going-Live Check", "Confirm SAP Enterprise Support entitlement, book the analysis session", "Oct 5 to 9"],
    ["Mine Mock-2 runtimes", "CFIN posting rates, job runtimes, load durations", "Oct 5 to 16"],
    ["Pull legacy volumes", "Infor LN GL, billing, Ariba, Pega and Control-M exports", "Oct 5 to 14"],
    ["AI triage of the inventory", "168 interfaces, RICEFW, Fiori and T-code usage", "Oct 7 to 14"],
    ["Call legacy owners", "Scale or stub: OneSource, PAC, Pega, legacy receivers", "Oct 7 to 16"],
    ["Stand up NeoLoad", "Controller, generators, network path to RISE, auth for perf users", "Oct 12 to 23"],
    ["Tier 1 sign-off workshop", "Risk scores, draft KPIs, owners per scenario", "Oct 15 to 16"],
  ];
  steps.forEach(([h, body, when], i) => {
    const cx = Math.floor(i / 5), cy = i % 5;
    const x = 0.556 + cx * 6.19, y = 1.55 + cy * 1.02;
    card(s, x, y, 6.03, 0.9);
    badge(s, x + 0.17, y + 0.2, 0.5, i + 1, BADGE_SEQUENCE[i % 4], 15);
    txt(s, h, { x: x + 0.85, y: y + 0.12, w: 3.6, h: 0.3, fontSize: 13.5, bold: true });
    txt(s, when, { x: x + 4.45, y: y + 0.12, w: 1.45, h: 0.3, fontSize: 11.5, bold: true, color: C.ORANGE, align: "right" });
    txt(s, body, { x: x + 0.85, y: y + 0.45, w: 5.05, h: 0.4, fontSize: 11.5, color: C.BODY_SLATE });
  });
}

// ------------------------------------------------------------------ 16 Team
{
  const s = content("Team and operating model", "About 13 FTE at peak, mostly ring-fenced so SIT2 and Mock teams are not drained");
  table(s, ["Role", "FTE", "Source"], [
    ["International performance test lead (owner)", "1.0", "International"],
    ["PwC performance test manager", "1.0", "PwC"],
    ["Performance engineers (NeoLoad scripting, execution)", "4.0", "Specialist partner or offshore"],
    ["Basis and HANA performance engineer", "1.0", "International or PwC, plus ECS"],
    ["ABAP performance developers (fix team)", "2.0", "PwC"],
    ["BTP Integration Suite engineer", "1.0", "Integration team"],
    ["Test data engineer (synthetic data factory)", "1.0", "PwC or partner"],
    ["DataStage and Control-M engineer", "0.5", "International"],
    ["Functional SMEs: OTC/VSM, CFIN, P2P/VIM, warranty, tax", "1.25", "5 x 25%, ring-fenced"],
    ["Security and GRC", "0.25", "International"],
    ["Legacy and SaaS owners", "named", "Infor LN, Pega, OneSource, PAC, OpenText, Ariba"],
  ], { x: 0.556, y: 1.55, w: 7.7, colW: [4.2, 0.8, 2.7], fontSize: 11, rowH: 0.42 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.55, y: 1.55, w: 4.23, h: 5.15, rectRadius: 0.08, fill: { color: C.NOTE_FILL }, line: { color: C.NOTE_BORDER, width: 0.75 } });
  txt(s, "CADENCE", { x: 8.75, y: 1.72, w: 3.9, h: 0.3, fontSize: 13, bold: true });
  const cad = [["Daily", "15-minute stand-up during cycles"], ["Twice weekly", "Performance defect triage with dev leads"], ["Weekly", "30-minute readout to VP IT and program"], ["Each cycle", "Results pack with PRD forecast"], ["Dec 4", "Go / no-go into tech go-live readiness"]];
  cad.forEach(([k, v], i) => {
    const y = 2.15 + i * 0.86;
    chip(s, 8.75, y, 1.35, 0.5, k, BADGE_SEQUENCE[i % 4], 11, i % 4 === 2 ? C.CHARCOAL : C.WHITE);
    txt(s, v, { x: 10.25, y, w: 2.4, h: 0.5, fontSize: 11.5, color: C.BODY_SLATE, valign: "middle" });
  });
  txt(s, "Detailed RACI and plan are in the workbook.", { x: 8.75, y: 6.32, w: 3.9, h: 0.3, fontSize: 11, color: C.MUTED_GRAY });
}

// ------------------------------------------------------------------ 17 RACI
{
  const s = content("RACI summary", "R responsible, A accountable, C consulted, I informed. The workbook carries the RACI for all 44 plan activities");
  const roles = ["VP IT / steering", "INTL perf lead", "PwC perf mgr", "Perf eng team", "Basis / HANA", "SAP ECS", "BTP integr.", "Func. SMEs", "Legacy owners", "Security / GRC"];
  const acts = [
    ["Charter, funding, decisions", "A", "R", "C", "I", "I", "I", "I", "I", "I", "I"],
    ["Tier 1 scope and risk scoring", "I", "A", "R", "C", "C", "", "C", "R", "C", ""],
    ["KPIs and acceptance criteria", "C", "A", "R", "C", "C", "", "C", "R", "I", ""],
    ["Pre-prod readiness and parity", "I", "A", "C", "C", "R", "R", "R", "", "", "C"],
    ["Perf users, roles, comm users", "", "A", "C", "C", "C", "", "C", "", "", "R"],
    ["Workload model and volumes", "", "A", "R", "R", "", "", "C", "C", "R", ""],
    ["Scripts, data, stubs", "", "A", "C", "R", "", "", "R", "C", "C", ""],
    ["Test execution cycles", "I", "A", "R", "R", "R", "C", "R", "C", "C", ""],
    ["Tuning and code fixes", "I", "A", "R", "C", "R", "C", "R", "C", "R", ""],
    ["Go / no-go recommendation", "A", "R", "R", "C", "C", "I", "C", "C", "I", "I"],
  ];
  const colors = { A: C.MAROON, R: C.ORANGE, C: C.CARD_GRAY, I: "F4F5F6", "": C.WHITE };
  const rows = [["Activity", ...roles].map(t => ({ text: t, options: { fill: { color: C.CHARCOAL }, color: C.WHITE, bold: true, fontSize: 9.5, fontFace: F.BODY, align: "center", valign: "middle" } }))];
  acts.forEach(r => rows.push(r.map((v, j) => j === 0
    ? { text: v, options: { fill: { color: C.WHITE }, color: C.CHARCOAL, bold: true, fontSize: 10.5, fontFace: F.BODY, valign: "middle" } }
    : { text: v, options: { fill: { color: colors[v] }, color: v === "A" ? C.WHITE : C.CHARCOAL, bold: true, fontSize: 11, fontFace: F.BODY, align: "center", valign: "middle" } })));
  s.addTable(rows, { x: 0.556, y: 1.55, w: 12.222, colW: [3.122, ...Array(10).fill(0.91)], rowH: 0.43, border: { type: "solid", pt: 0.75, color: C.WHITE }, margin: [2, 4, 2, 4] });
}

// ------------------------------------------------------------------ 18 Risks
{
  const s = content("Top risks and mitigations", "Owned by the performance lead and reviewed at each weekly readout");
  table(s, ["Risk", "Rating", "Mitigation"], [
    ["Pre-prod contention with cutover rehearsal and UAT", "High", "Reserve Nov 2 to Dec 4 now. Slot nights and weekends. Option C as contingency"],
    ["Team pulled into SIT2 and Mock-2 firefighting", "High", "Dedicated external performance team. SMEs ring-fenced at 25%"],
    ["Volumes unknown today", "High", "Mine legacy data in week 1. Conservative 1.5x headroom, flagged as assumption"],
    ["Legacy and SaaS endpoints cannot take load", "High", "Stub with mock iFlows. Separate low-rate contract test against the real endpoint"],
    ["Fixes arrive too late to retest", "High", "Shift-left in SIT2. Twice-weekly triage. Priority transport lane for performance fixes"],
    ["Pre-prod data not production-shaped", "Medium", "Refresh from Mock load. Check table sizes against PRD projection"],
    ["Scaling misread leads to false confidence", "Medium", "Three-class model, ECS config sheet, calibration run, class C at full load"],
    ["SSO blocks scripted performance users", "Medium", "Agree the authentication approach for performance users in week 2"],
    ["Defect that cannot be fixed by Dec 15", "Medium", "Pre-agreed workarounds (scheduling, parallelization) plus hypercare alerts"],
  ], { y: 1.55, colW: [4.3, 1.1, 6.822], fontSize: 11.5, rowH: 0.52 });
}

// ------------------------------------------------------------------ 19 Decisions
{
  const s = content("Decisions needed by Oct 9", "Each week of delay comes straight out of the execution window");
  const ds = [
    ["Stand up performance assurance as a funded workstream", "Named International owner, PwC counterpart, change request approved"],
    ["Bring in a specialist performance team of about 6 people", "So SIT2, Mock-2 and UAT staff are not diverted"],
    ["Reserve pre-prod Nov 2 to Dec 4", "Agree slots with the cutover lead. Approve the Mock data refresh and snapshots through ECS"],
    ["Direct legacy and SaaS owners to commit capacity or accept stubs by Oct 16", "Infor LN, Pega, OneSource, Mexico PAC, OpenText, legacy receivers"],
    ["Make the Dec 4 performance gate a formal input to tech go-live readiness", "KPIs signed by process owners by Oct 23"],
  ];
  ds.forEach(([h, body], i) => {
    const y = 1.6 + i * 1.03;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.667, y, w: 12.0, h: 0.9, rectRadius: 0.068, fill: { color: C.CARD_GRAY }, line: { color: C.CARD_GRAY } });
    badge(s, 0.97, y + 0.17, 0.556, i + 1, BADGE_SEQUENCE[i % 4], 20);
    txt(s, h, { x: 1.806, y: y + 0.13, w: 10.6, h: 0.33, fontSize: 15, bold: true, valign: "middle" });
    txt(s, body, { x: 1.806, y: y + 0.5, w: 10.6, h: 0.3, fontSize: 12.5, color: C.BODY_SLATE, valign: "middle" });
  });
}

// ------------------------------------------------------------------ 20 Appendix hotspots
{
  const s = content("Appendix: technical hotspots to probe first", "Architecture-level checks that most often decide SAP go-live performance. Each is a shift-left item in SIT2");
  table(s, ["Area", "What to check"], [
    ["Number ranges", "Buffering for FI, billing and eDocument numbers. Non-buffered or gapless ranges for Mexico serialize postings"],
    ["OneSource", "Synchronous call per item in order, billing and invoice verification. Connection pooling, timeouts, vendor rate limits"],
    ["Billing chain", "Billing run, then output forms, then DRC eDocument, then PAC. Throughput of the slowest link sets invoices per hour"],
    ["CFIN via DataStage JDBC", "Commit size, parallel streams, staging table indexes and locks, AIF parallel posting, recon report runtime"],
    ["Integration Suite", "Tenant message limits, JMS capacity, EOIO serialization, large payload memory, retry storms, Cloud Connector HA"],
    ["VIM", "OCR throughput, DP document jobs, workflow event queue, duplicate check, background job schedule"],
    ["VSM and AVC", "Model complexity, dependency evaluation, pricing condition volume, BOM explosion on save"],
    ["Fiori and identity", "Launchpad catalog size per role, OData batching, SSO for load users, Web Dispatcher limits"],
    ["HANA", "Table sizes from Mock data, ACDOCA reads, expensive statements, delta merge, memory allocation limit"],
    ["Batch", "Control-M concurrency versus background work processes, job classes, overlap with US and Mexico online peaks"],
  ], { y: 1.55, colW: [2.4, 9.822], fontSize: 11, rowH: 0.48 });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
