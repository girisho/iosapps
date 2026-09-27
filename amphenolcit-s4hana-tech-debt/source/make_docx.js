const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, HeadingLevel, LevelFormat, BorderStyle, Footer, PageNumber, Header,
} = require("docx");

const OUT = process.argv[2];
const DARK = "17313B", TEAL = "0F766E", TINT = "E6F2F0", AMBER_T = "FEF3C7", GREY = "F3F4F6";
const FONT = "Calibri";
const W = 12240 - 2 * 1080; // letter width minus 0.75" margins = 10080 DXA

const run = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 20, bold: o.bold, italics: o.italics, color: o.color });
const P = (text, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 100, before: o.before ?? 0 }, keepNext: o.keepNext,
  alignment: o.align,
  children: Array.isArray(text) ? text : [run(text, o)],
});
const rich = (parts, o = {}) => P(parts.map(p => typeof p === "string" ? run(p, o) : run(p[0], { ...o, bold: true })), o);
const H1 = (t, br) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: !!br, keepNext: true, keepLines: true, spacing: { before: 240, after: 120 }, children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: DARK })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 180, after: 80 }, children: [new TextRun({ text: t, font: FONT, size: 24, bold: true, color: TEAL })] });
const B = (parts, lvl = 0) => new Paragraph({
  numbering: { reference: "bullets", level: lvl }, spacing: { after: 60 },
  children: (Array.isArray(parts) ? parts : [parts]).map(p => typeof p === "string" ? run(p) : run(p[0], { bold: true })),
});
const N = (parts) => new Paragraph({
  numbering: { reference: "numbers", level: 0 }, spacing: { after: 60 },
  children: (Array.isArray(parts) ? parts : [parts]).map(p => typeof p === "string" ? run(p) : run(p[0], { bold: true })),
});

const border = { style: BorderStyle.SINGLE, size: 4, color: "D1D5DB" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(headers, rows, widths, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (txt, w, isHdr, shade) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: isHdr ? { type: ShadingType.CLEAR, fill: DARK, color: "auto" } : (shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined),
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: String(txt).split("|").map(line => new Paragraph({
      spacing: { after: 20 },
      children: [new TextRun({ text: line, font: FONT, size: o.size || 17, bold: isHdr || (o.boldFirst && shade === TINT), color: isHdr ? "FFFFFF" : "1F2937" })],
    })),
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, widths[i], true)) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], false, i === 0 && o.boldFirst ? TINT : (ri % 2 ? GREY : undefined))) })),
    ],
  });
}
const callout = (title, lines, fill = TINT) => new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [W],
  rows: [new TableRow({ children: [new TableCell({
    width: { size: W, type: WidthType.DXA }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
    shading: { type: ShadingType.CLEAR, fill, color: "auto" }, margins: { top: 120, bottom: 120, left: 180, right: 180 },
    children: [new Paragraph({ spacing: { after: 60 }, children: [run(title, { bold: true, color: DARK, size: 21 })] }),
      ...lines.map(l => new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 40 }, children: (Array.isArray(l) ? l : [l]).map(p => typeof p === "string" ? run(p) : run(p[0], { bold: true })) }))],
  })] })],
});
const gap = () => P("", { after: 80 });

const children = [
  new Paragraph({ spacing: { after: 40 }, children: [run("AmphenolCIT  |  SAP S/4HANA Post-Go-Live Program  |  Enterprise Architecture", { size: 18, color: TEAL, bold: true })] }),
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Tech Debt Collection", font: FONT, size: 48, bold: true, color: DARK })] }),
  new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Quick Reference Guide for workshops, interviews and system analysis", font: FONT, size: 26, color: "4B5563" })] }),
  P("Draft v0.1  |  September 2026  |  Companion to: S/4HANA Tech Debt & Innovation Strategy deck and the Tech Debt Planner workbook", { size: 17, italics: true, color: "6B7280", after: 200 }),

  callout("The five golden rules", [
    [["One backlog. "], "Features, defects, tech debt, enablers and risk items all go in the same register so they compete for the same capacity."],
    [["Evidence over opinion. "], "Attach a transaction, report, ATC result, screenshot or usage number to every item."],
    [["Name the interest. "], "State what the debt costs every month (hours, incidents, blocked features). No interest, low priority."],
    [["Every item has a business owner. "], "IT owns the fix, the business owns the value and the priority argument."],
    [["Small is fine, vague is not. "], "A 10-minute workaround logged today beats a perfect item logged never. Use the minimum data set (Section 4)."],
  ]),

  H1("1. Is it a feature, a defect or tech debt?"),
  P("Classify before you score. Use the first question that answers “yes”."),
  table(["Type", "Test question", "AmphenolCIT example", "Route"], [
    ["Defect", "Does something not work as designed or as it did before?", "EDI ORDERS IDocs fail with status 51", "P1/P2: expedite lane, bypass ranking. P3/P4: backlog with WSJF"],
    ["Risk / Compliance", "Is there a deadline, audit, security or maintenance-end driver?", "Behind latest Feature Pack; PI/PO maintenance horizon", "Backlog; high Time Criticality score"],
    ["Tech Debt", "Does it work today but make every future change slower, riskier or impossible?", "Business data held in Z-fields that Fiori apps and APIs cannot see", "Backlog; score Interest + Principal and WSJF"],
    ["Enabler", "Is it platform or architecture work that other items depend on?", "Work Zone subaccount + IdP; Integration Suite landing zone", "Backlog; high Opportunity Enablement score"],
    ["Feature", "Does it add or improve a business capability?", "Monitor Material Coverage app for planners", "Backlog; WSJF"],
  ], [1500, 3100, 3000, 2480], { boldFirst: true }),

  H1("2. Where to look: seven categories of S/4HANA tech debt"),
  P("Mapped to SAP’s clean core dimensions (Processes, Extensibility, Data, Integration, Operations) plus user experience and quality."),
  table(["Category", "Symptoms you hear", "Evidence: tool / transaction", "Typical fix pattern"], [
    ["Custom code & modifications|(Extensibility)", "“Upgrades take months”, “only one developer understands it”",
      "ATC with clean-core / ABAP Cloud readiness checks; SCMON / SUSG usage data; SE95 modification browser; SPAU/SPDD history; Custom Code Migration app",
      "Retire unused code first; move modifications to released BAdIs; new builds in ABAP Cloud (on-stack) or on BTP (side-by-side)"],
    ["User experience|(UX)", "“We still use GUI”, “Fiori is slow / not set up”",
      "ST03N transaction usage; SAP Innovation & Optimization Pathfinder; Fiori Apps Reference Library (search by transaction); FLP configuration and role catalogs",
      "Role-based spaces/pages; wave rollout of recommended apps; Work Zone as single entry point"],
    ["Integration", "“We find failures when the customer calls”, point-to-point files",
      "SM59 RFC destinations; WE20 partner profiles; BD87 / WE02 IDoc errors; PI/PO ICO list; Integration Suite Migration Assessment; ISA-M",
      "Classify with ISA-M; standard APIs/events first; migrate in waves to Integration Suite; central monitoring in Cloud ALM"],
    ["Data & custom fields|(Data)", "“The report never matches”, data kept in Z-fields or Excel",
      "SE11 append structures (ZZ*/YY*); Custom Fields app; data profiling / DQ rules; duplicate BP checks; MDG or Information Steward if available",
      "Map Z-fields to standard fields where one exists; otherwise expose via Custom Fields app (CDS/OData); DQ rules + data owners"],
    ["Process workarounds|(Processes)", "“We do that in a spreadsheet”, manual month-end steps",
      "SAP Signavio Process Insights; process mining; interviews; count of manual journal entries / re-keyed orders",
      "Adopt standard S/4 functionality and best practices; automate with Build Process Automation only after standard is exhausted"],
    ["Platform, release & ops|(Operations)", "“We’re afraid to patch”, manual transports",
      "Current release/FPS vs latest; SAP Readiness Check; SM37 job failures; ST22 dumps; SUIM role design; Cloud ALM health & job monitoring",
      "Annual release/FPS rhythm; Cloud ALM Change & Deployment; automated monitoring and alerting"],
    ["Testing & knowledge|(Quality)", "“Testing takes 3 weeks”, no current documentation",
      "Regression test inventory; % automated; documentation age; single-person dependencies",
      "Automate top end-to-end processes; living documentation in Cloud ALM; pair and rotate"],
  ], [1560, 2000, 3520, 3000], { boldFirst: true, size: 16 }),

  H1("3. SAP clean core extensibility levels (use in the register)"),
  P("SAP’s current extensibility guidance classifies every extension from A (cleanest) to D (avoid). Record the level of each custom object or item; the trend of C/D items is a headline KPI. Verify against SAP’s latest extensibility guide as definitions are refined over time.", { after: 100 }),
  table(["Level", "What it means", "Example", "Action"], [
    ["A", "ABAP Cloud / released APIs and extension points; key-user extensibility; side-by-side on BTP", "Custom field added via Custom Fields app; RAP BO on released CDS", "Target state for all new work"],
    ["B", "Classic ABAP using classic APIs SAP lists as stable", "Report calling a classic BAPI", "Acceptable; monitor"],
    ["C", "Uses SAP-internal / unreleased objects; may break on upgrade", "Direct SELECT on internal tables; unreleased function modules", "Remediate when touched or when interest is high"],
    ["D", "Not recommended: modifications, implicit enhancements, direct writes to SAP tables", "Code in MV45AFZZ user exits, core modifications", "Top priority to retire or refactor"],
  ], [900, 3780, 3000, 2400], { boldFirst: true }),

  H1("4. Minimum data set to capture (maps to the Planner register)"),
  table(["Field", "What to enter", "Example"], [
    ["Title", "Verb + object, max ~12 words", "Expose sales region Z-field via Custom Fields app"],
    ["Item type", "Feature / Defect / Tech Debt / Enabler / Risk-Compliance (Section 1)", "Tech Debt"],
    ["Clean core dimension", "Process / Extensibility / Data / Integration / Operations / UX", "Data"],
    ["Area / module", "FI, CO, SD, MM, PP, QM, PM, EWM, Basis, BTP, Integration", "SD"],
    ["Description / symptom", "What happens, who is affected, how often", "Credit reports disagree with sales dashboard every week"],
    ["Evidence", "Transaction, ATC finding, object name, screenshot, usage count", "SE11: KNVV append ZZREGION; 4,200 records"],
    ["Root cause (Fowler quadrant)", "Deliberate or inadvertent; prudent or reckless", "Deliberate-Prudent (go-live shortcut)"],
    ["Clean core level", "A / B / C / D / n/a (Section 3)", "C"],
    ["Blocks innovation?", "Y if it prevents Fiori, Work Zone, APIs, analytics or AI use", "Y - standard app cannot show region"],
    ["Interest", "Hours per month lost to workarounds, incidents, extra testing", "12 hrs/month"],
    ["Principal", "Person-days to remove", "8"],
    ["WSJF inputs", "Business Value, Time Criticality, Risk Reduction/Opportunity Enablement, Job Size (Section 5)", "5 / 3 / 8 / 3"],
    ["Owners", "Business owner + IT owner (named people)", "Sales ops lead / Data lead"],
    ["Target quarter / status", "Set by triage, not by the requester", "Q1-2027 / Triaged"],
  ], [2300, 4580, 3200], { boldFirst: true }),

  H1("5. Scoring cheat sheet"),
  H2("WSJF (Weighted Shortest Job First, SAFe)"),
  callout("WSJF = (Business Value + Time Criticality + Risk Reduction / Opportunity Enablement) ÷ Job Size", [
    "Score each factor relatively on 1 – 2 – 3 – 5 – 8 – 13 – 20. Put the smallest item in the batch at 1 and score the rest against it.",
    "Score one column at a time across all items (not one item at a time). This keeps scores consistent.",
    "Tech debt rarely wins on Business Value; it wins on Risk Reduction / Opportunity Enablement. Score that honestly.",
  ], AMBER_T),
  gap(),
  table(["Score", "Business Value", "Time Criticality", "Risk Reduction / Opp. Enablement", "Job Size"], [
    ["1", "Nice to have, few users", "No deadline; value does not decay", "No risk change; unlocks nothing", "Hours to a couple of days"],
    ["3", "Saves one team noticeable effort", "Helpful before next quarter-end", "Reduces a minor risk or unblocks one item", "About a sprint for one person"],
    ["8", "Measurable KPI gain for a function", "Tied to month-end, audit or a contract date", "Removes upgrade/security risk or unblocks an epic (e.g. Fiori wave)", "Multi-sprint, one team"],
    ["20", "Strategic, enterprise-wide value", "Hard deadline; missing it has penalties", "Prerequisite for a strategic program (Work Zone, AI, integration migration)", "Multi-team / multi-quarter: split it"],
  ], [900, 2300, 2300, 2580, 2000], { boldFirst: true }),
  H2("Interest vs principal (tech debt only)"),
  B([["Annual interest cost"], " = interest hrs/month × 12 × day rate ÷ 8.  ", ["Payback"], " = principal cost ÷ monthly interest cost."]),
  B([["High interest + low principal"], " → pay down now.  ", ["High + high"], " → plan an epic.  ", ["Low + low"], " → fix when you touch it (Boy Scout rule).  ", ["Low + high"], " → accept and document."]),
  H2("Defect severity"),
  table(["Severity", "Definition", "Route", "Target response"], [
    ["P1", "Production down or critical process stopped; no workaround", "Expedite lane, swarm, outside sprint", "Immediate; fix within 1 day"],
    ["P2", "Major process degraded; costly workaround", "Expedite lane", "Fix within current sprint"],
    ["P3", "Moderate impact; workaround acceptable", "Backlog, WSJF ranked", "Scheduled by ranking"],
    ["P4", "Cosmetic / minor", "Backlog; batch with related work", "Opportunistic"],
  ], [1100, 3700, 2900, 2380], { boldFirst: true }),
  P("Response targets are proposals; align them with your AMS contract and ITSM SLAs.", { size: 16, italics: true, color: "6B7280", before: 60 }),

  H1("6. Custom-field deep dive (AmphenolCIT priority)", true),
  P("Because business data sits in custom fields, run this checklist per Z-field. Record the answers in the register’s Notes / evidence column or a linked sheet."),
  table(["#", "Question", "Why it matters"], [
    ["1", "Which table / structure and field? (e.g. MARA append, KNVV append, VBAK)", "Scope and technical owner"],
    ["2", "What business meaning does it hold, and who owns that meaning?", "Data ownership; stops duplicate definitions"],
    ["3", "How many records are populated, and how complete / valid are they?", "Data quality baseline"],
    ["4", "Does S/4HANA now have a standard field or object for the same meaning?", "If yes: migrate to standard and retire the Z-field"],
    ["5", "Where is it used: reports, forms, interfaces, pricing, workflow, BW/analytics?", "Blast radius of any change"],
    ["6", "Is it visible in CDS views, OData services and Fiori apps today?", "If not: standard apps, APIs and Work Zone cannot use it"],
    ["7", "Was it created via SE11 append or the Custom Fields app?", "Custom Fields app = Level A, automatically exposed to UIs/APIs"],
    ["8", "Decision: Map to standard / Re-create via Custom Fields app / Keep & wrap in CDS / Retire", "Drives the register item and effort"],
  ], [500, 5580, 4000]),

  H1("7. Interview question bank"),
  P("Use 3–5 questions per session. Always end with: “What would you stop doing tomorrow if IT fixed one thing?”"),
  H2("Business users & key users"),
  B("Which tasks do you still do in SAP GUI, Excel or email that you expected S/4HANA to do for you?"),
  B("Where do you re-key or cross-check data between systems or reports?"),
  B("Which reports do you not trust, and which number do you use instead?"),
  B("Have you seen Fiori apps or Work Zone? What would you want on your home page?"),
  H2("Business process owners"),
  B("Which S/4HANA capabilities were descoped at go-live and are still missing?"),
  B("What are the top three process KPIs you cannot measure today?"),
  B("Which month-end, quarter-end or audit steps are manual and risky?"),
  H2("Functional consultants / AMS"),
  B("Which tickets come back every month? What is the underlying cause?"),
  B("Which configuration or custom objects were go-live shortcuts meant to be temporary?"),
  B("Which Z-fields hold data that has a standard home in S/4HANA?"),
  H2("ABAP developers"),
  B("Which objects are modifications or implicit enhancements? Which are touched on every change?"),
  B("What does ATC report with clean-core checks? How many findings are Level C or D?"),
  B("Which custom code has no usage in SCMON/SUSG data over 12 months?"),
  H2("Basis, BTP & security"),
  B("What release and Feature Pack are we on, and when was the last SP/FPS applied?"),
  B("Is the Fiori front-end server embedded or hub? Are Fiori roles and catalogs designed per job role?"),
  B("Do we have a BTP global account, entitlements (e.g. BTPEA/CPEA credits), Cloud Identity Services and Cloud Connector in place?"),
  B("Is SAP Cloud ALM activated? Which apps are in use (requirements, test, monitoring, change & deployment)?"),
  H2("Integration team"),
  B("How many interfaces, by technology (IDoc, RFC, file, SOAP, REST, PI/PO)? Which fail most?"),
  B("Who is told when an interface fails, and how long until they know?"),
  B("Which interfaces could use a standard SAP API or event instead of a custom one?"),
  H2("Data owners"),
  B("Which master data domains cause the most errors (business partner, material, pricing)?"),
  B("Who approves master data changes today? Is there a governance workflow?"),
  B("Do we measure data quality? What is the current score for your domain?"),

  H1("8. From collection to backlog in five steps"),
  N([["Capture"], " in the register using the minimum data set (Section 4) — within 48 hours of the workshop."]),
  N([["Deduplicate and classify"], " at the weekly triage: item type, dimension, severity, clean core level."]),
  N([["Size and score"], " at refinement: WSJF inputs, interest and principal, business and IT owner confirmed."]),
  N([["Rank and allocate"], " at the monthly portfolio review against capacity guardrails for each work type."]),
  N([["Show it"], ": board, KPI dashboard and sprint demo. Re-score quarterly; close anything stale older than 90 days."]),
  H2("Do’s and don’ts"),
  table(["Do", "Don’t"], [
    ["Log workarounds as tech debt with their monthly cost", "Keep a separate “tech debt list” nobody prioritises"],
    ["Link each item to the clean core dimension and level", "Score everything 20; relative scoring only works if you use the full scale"],
    ["Retire unused code before remediating it", "Remediate code nobody runs"],
    ["Bundle debt with the feature that touches the same object", "Start large refactors without a business owner"],
    ["Use SAP standard and released APIs first", "Build new Z-tables or modifications without design authority approval"],
  ], [5040, 5040]),
  P("", { after: 60 }),
  P("Sources and further reading: SAP clean core guidance and extensibility guide (SAP Community / SAP Help); SAP Activate methodology; SAP Cloud ALM documentation; SAP Integration Solution Advisory Methodology (ISA-M); SAFe WSJF and capacity allocation; Flow Framework (M. Kersten); Technical Debt Quadrant (M. Fowler).", { size: 16, italics: true, color: "6B7280" }),
];

const doc = new Document({
  creator: "Enterprise Architecture", title: "Tech Debt Collection - Quick Reference Guide",
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1000, bottom: 1000, left: 1080, right: 1080 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run("Tech Debt Collection – Quick Reference Guide", { size: 16, color: "9CA3AF" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Draft for discussion  |  Page ", font: FONT, size: 16, color: "9CA3AF" }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "9CA3AF" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("wrote", OUT); });
