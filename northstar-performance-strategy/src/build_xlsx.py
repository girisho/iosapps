#!/usr/bin/env python3
"""NorthStar Performance Assurance workbook: plan, RACI, catalogs and models."""
import datetime as dt
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else "plan.xlsx"
D = dt.date

CH, OR, MA, BL, ST = "272623", "FF7144", "5C1916", "0062A2", "4E5659"
CARD, ZEB, MUTED, NOTE = "E8E9EB", "EAF1F4", "82817D", "EEF2F7"
INPUT = "FFF2CC"

F = lambda **k: Font(name="Arial", size=k.pop("size", 10), **k)
fill = lambda c: PatternFill("solid", start_color=c, end_color=c)
thin = Side(style="thin", color="D5D8DC")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

wb = Workbook()


def title(ws, text, sub=None, width=10):
    ws["A1"] = text
    ws["A1"].font = F(size=16, bold=True, color=CH)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = F(size=10, italic=True, color=MUTED)
    ws.sheet_view.showGridLines = False


def header(ws, row, cols, start=1, color=CH):
    for i, h in enumerate(cols):
        c = ws.cell(row=row, column=start + i, value=h)
        c.font = F(bold=True, color="FFFFFF")
        c.fill = fill(color)
        c.alignment = CENTER
        c.border = BOX


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[L(i)].width = w


def body(ws, r, c, v, bold=False, inp=False, fmt=None, center=False, zebra=False, color=CH):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = F(bold=bold, color=("0000FF" if inp else color))
    cell.border = BOX
    cell.alignment = CENTER if center else WRAP
    if inp:
        cell.fill = fill(INPUT)
    elif zebra:
        cell.fill = fill(ZEB)
    if fmt:
        cell.number_format = fmt
    return cell


def dv_list(ws, items, rng):
    dv = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


# ====================================================================== Read Me
ws = wb.active
ws.title = "Read Me"
title(ws, "Project NorthStar  |  Performance Assurance Workbook", "Companion to the Performance Assurance Strategy deck. Draft, October 2026.")
widths(ws, [24, 110])
rows = [
    ("Purpose", "One place to plan, staff, scope and track the NorthStar performance test workstream from mobilization (Oct 5, 2026) through the first month-end close after business go-live."),
    ("Key dates", "UAT Oct 26 to Nov 20. Cutover from Nov 23. Tech go-live Dec 15, 2026. Business go-live Jan 1, 2027. Performance go / no-go gate Dec 4."),
    ("Environment fact", "Pre-prod is sized at about 50% of PRD (per VP IT). Confirm the exact configuration with SAP ECS and enter it on the Scaling Model tab."),
    ("Plan", "Phased plan with weekly Gantt. Edit Start, End, Status and % Complete. Bars and milestones redraw automatically."),
    ("RACI", "R, A, C, I by role for every plan activity. The check column flags any row without exactly one A."),
    ("Scenario Catalog", "Tier 1 (35) and example Tier 2 scenarios with risk scoring, KPIs and owners. Scores 1 to 5; Suggested Tier is calculated."),
    ("Workload Model", "Turns daily volumes into peak-hour design load, pre-prod step targets and virtual users. Yellow cells are inputs."),
    ("Scaling Model", "Pre-prod versus PRD configuration, the capacity ratio, and PRD projections by metric class (A, B, C)."),
    ("KPI Library", "Proposed default thresholds by metric class and where each is measured."),
    ("Interface Inventory", "Template for the 168 BTP interfaces with risk score and suggested tier."),
    ("Batch Inventory", "Template for Control-M, SAP, DataStage and SOA jobs on the critical path."),
    ("Env Readiness", "Entry checklist for pre-prod before cycle 1 (target Nov 2)."),
    ("Risks and Decisions", "Risk log with scoring and the decision log for leadership."),
    ("Team", "Roles, FTE, source and FTE-weeks."),
    ("", ""),
    ("Cell legend", "Yellow fill with blue text = input you are expected to edit. Black text = formula or fixed content. Do not overwrite formula cells."),
    ("Role codes", "VP = VP IT and steering  |  IPL = International performance test lead  |  PPM = PwC performance test manager  |  PET = performance engineering team  |  TDE = test data engineer  |  BAS = Basis and HANA  |  ECS = SAP ECS (RISE)  |  BTP = BTP integration team  |  ABAP = ABAP fix team  |  DSC = DataStage and Control-M  |  SME = functional SMEs  |  LEG = legacy and SaaS owners  |  SEC = security and GRC  |  CUT = cutover lead"),
    ("Assumptions", "Volumes, peak profiles and KPI thresholds are proposals until mined and signed (target Oct 14 and Oct 23). Example values are marked as examples."),
]
for i, (k, v) in enumerate(rows, start=4):
    ws.cell(row=i, column=1, value=k).font = F(bold=True)
    c = ws.cell(row=i, column=2, value=v)
    c.font = F()
    c.alignment = WRAP
ws["A19"].fill = fill(INPUT)
ws["A19"].font = F(bold=True, color="0000FF")

# ====================================================================== Plan
ROLES = ["VP", "IPL", "PPM", "PET", "TDE", "BAS", "ECS", "BTP", "ABAP", "DSC", "SME", "LEG", "SEC", "CUT"]
# id, phase, task, R, A, start, end, type, C-roles, I-roles
T, M = "Task", "Milestone"
PLAN = [
    ("0", "Phase 0  Mobilize", None),
    ("0.1", "Mobilize", "Name International performance test lead and PwC performance manager", "VP", "VP", D(2026, 10, 5), D(2026, 10, 6), T, "PPM", "SME"),
    ("0.2", "Mobilize", "Present strategy; obtain steering approval and funding", "IPL", "VP", D(2026, 10, 6), D(2026, 10, 9), T, "PPM", "SME,BAS,BTP"),
    ("0.3", "Mobilize", "Raise PwC change request for the performance workstream", "PPM", "VP", D(2026, 10, 5), D(2026, 10, 14), T, "IPL", ""),
    ("0.4", "Mobilize", "Contract specialist performance engineers and test data engineer", "IPL", "VP", D(2026, 10, 7), D(2026, 10, 16), T, "PPM", ""),
    ("0.5", "Mobilize", "ECS tickets: pre-prod and PRD config sheet, refresh plan, snapshots, upsize quote", "BAS", "IPL", D(2026, 10, 5), D(2026, 10, 16), T, "ECS", "PPM"),
    ("0.6", "Mobilize", "Request SAP Going-Live Check (confirm Enterprise Support entitlement)", "BAS", "IPL", D(2026, 10, 5), D(2026, 10, 9), T, "ECS", "VP"),
    ("0.7", "Mobilize", "Agree pre-prod slot plan with cutover lead for Nov 2 to Dec 4", "IPL", "VP", D(2026, 10, 7), D(2026, 10, 9), T, "CUT,BAS", "PPM"),
    ("0.8", "Mobilize", "Legacy and SaaS owners decide: scale test instance or accept stub", "LEG", "IPL", D(2026, 10, 7), D(2026, 10, 16), T, "BTP,PPM", "VP"),
    ("M0", "Mobilize", "Steering approval, workstream launched", "IPL", "VP", D(2026, 10, 9), D(2026, 10, 9), M, "", "PPM"),
    ("1", "Phase 1  Shift-left baselines (SIT2)", None),
    ("1.1", "Shift-left", "Enable telemetry in SIT2: ST03N and STAD retention, SQLM, HANA expensive statements, IS trace", "BAS", "IPL", D(2026, 10, 5), D(2026, 10, 9), T, "BTP", "PPM"),
    ("1.2", "Shift-left", "Analyze Mock-2 runtimes: CFIN JE posting rate, load durations, job runtimes", "BAS", "PPM", D(2026, 10, 5), D(2026, 10, 16), T, "DSC,SME", "IPL"),
    ("1.3", "Shift-left", "Single-user baselines of Tier 1 transactions during SIT2", "PET", "PPM", D(2026, 10, 12), D(2026, 10, 23), T, "SME", "IPL"),
    ("1.4", "Shift-left", "Interface latency baselines: OneSource, DRC and PAC, Pega, Ariba", "BTP", "PPM", D(2026, 10, 12), D(2026, 10, 23), T, "LEG", "IPL"),
    ("1.5", "Shift-left", "Expensive SQL and custom code review: VIM, CFIN and AIF, VSM, enhancements", "ABAP", "PPM", D(2026, 10, 12), D(2026, 10, 30), T, "BAS,SME", "IPL"),
    ("1.6", "Shift-left", "Technical hotspot checks: number ranges, IS limits, Cloud Connector, HANA parameters", "BAS", "IPL", D(2026, 10, 12), D(2026, 10, 23), T, "BTP,ECS", "PPM"),
    ("2", "Phase 2  Design and build", None),
    ("2.1", "Design and build", "Collect inventory: 168 interfaces, RICEFW, Fiori and T-code usage, Control-M export", "PPM", "IPL", D(2026, 10, 5), D(2026, 10, 9), T, "BTP,DSC,SME", ""),
    ("2.2", "Design and build", "AI-assisted classification and draft risk scores", "PET", "IPL", D(2026, 10, 7), D(2026, 10, 14), T, "PPM,BTP", ""),
    ("2.3", "Design and build", "Tier 1 sign-off workshop", "IPL", "IPL", D(2026, 10, 15), D(2026, 10, 16), T, "PPM,SME,BTP,BAS,LEG", "VP"),
    ("M2a", "Design and build", "Tier 1 scope signed", "IPL", "IPL", D(2026, 10, 16), D(2026, 10, 16), M, "", "VP"),
    ("2.4", "Design and build", "Mine legacy volumes and build the workload model", "TDE", "PPM", D(2026, 10, 7), D(2026, 10, 21), T, "LEG,DSC,SME", "IPL"),
    ("2.5", "Design and build", "KPI and acceptance criteria sign-off by process owners", "PPM", "IPL", D(2026, 10, 19), D(2026, 10, 23), T, "SME,BAS", "VP"),
    ("2.6", "Design and build", "NeoLoad infrastructure: controller, generators, network path to RISE, auth for perf users", "PET", "PPM", D(2026, 10, 12), D(2026, 10, 23), T, "BAS,ECS,SEC", "IPL"),
    ("2.7", "Design and build", "Performance users and roles cloned from production roles; communication users", "SEC", "IPL", D(2026, 10, 19), D(2026, 10, 30), T, "BAS,BTP,PET", ""),
    ("2.8", "Design and build", "Service virtualization stubs (mock iFlows) for endpoints that cannot take load", "BTP", "PPM", D(2026, 10, 19), D(2026, 10, 30), T, "LEG,PET", "IPL"),
    ("2.9", "Design and build", "Synthetic data factory: JEs, VSM configurations, invoices, VIM images, warranty claims", "TDE", "PPM", D(2026, 10, 19), D(2026, 11, 4), T, "SME,PET", "IPL"),
    ("2.10", "Design and build", "Script Tier 1 UI scenarios (Fiori and SAP GUI)", "PET", "PPM", D(2026, 10, 19), D(2026, 11, 4), T, "SME", "IPL"),
    ("2.11", "Design and build", "Build non-UI injectors: iFlow payloads, JDBC JE volumes, file drops", "PET", "PPM", D(2026, 10, 19), D(2026, 10, 30), T, "BTP,DSC", "IPL"),
    ("2.12", "Design and build", "Control-M batch replay schedule for the critical path", "DSC", "PPM", D(2026, 10, 26), D(2026, 11, 4), T, "PET,BAS", "IPL"),
    ("2.13", "Design and build", "Pre-prod refresh with Mock data plus config and transport parity", "BAS", "IPL", D(2026, 10, 26), D(2026, 10, 30), T, "ECS,CUT", "PPM"),
    ("2.14", "Design and build", "Monitoring dashboards (Cloud ALM, IS, HANA) and results template", "BAS", "IPL", D(2026, 10, 26), D(2026, 10, 30), T, "BTP,PET", "PPM"),
    ("2.15", "Design and build", "Calibration run and scaling factor confirmation", "PET", "IPL", D(2026, 11, 2), D(2026, 11, 3), T, "BAS,ECS", "PPM"),
    ("M2b", "Design and build", "Ready to execute: pre-prod entry criteria met", "IPL", "IPL", D(2026, 11, 2), D(2026, 11, 2), M, "", "VP"),
    ("3", "Phase 3  Execute in pre-prod", None),
    ("3.1", "Execute", "Cycle 1: component and interface throughput (CFIN JE, top iFlows, VIM, OneSource, DRC)", "PET", "PPM", D(2026, 11, 3), D(2026, 11, 6), T, "BAS,BTP,DSC", "IPL"),
    ("3.2", "Execute", "Cycle 2: integrated peak hour (online plus interfaces)", "PET", "PPM", D(2026, 11, 9), D(2026, 11, 13), T, "BAS,BTP,SME", "IPL"),
    ("3.3", "Execute", "Cycle 3: month-end close and batch critical path", "PET", "PPM", D(2026, 11, 12), D(2026, 11, 18), T, "DSC,BAS,SME", "IPL"),
    ("3.4", "Execute", "Cycle 4: stress to break point and 8-hour soak", "PET", "PPM", D(2026, 11, 16), D(2026, 11, 20), T, "BAS,BTP", "IPL"),
    ("3.5", "Execute", "Twice-weekly defect triage and tuning", "ABAP", "PPM", D(2026, 11, 3), D(2026, 12, 4), T, "BAS,BTP,LEG,PET", "IPL"),
    ("3.6", "Execute", "Results pack with PRD forecast after each cycle", "PPM", "IPL", D(2026, 11, 6), D(2026, 11, 20), T, "PET,BAS", "VP"),
    ("4", "Phase 4  Retest and gate", None),
    ("4.1", "Retest and gate", "Retest failed Tier 1 scenarios after fixes", "PET", "PPM", D(2026, 11, 23), D(2026, 12, 2), T, "ABAP,BAS,CUT", "IPL"),
    ("4.2", "Retest and gate", "Performance test summary report and PRD forecast", "PPM", "IPL", D(2026, 12, 1), D(2026, 12, 3), T, "PET,BAS", "VP"),
    ("M4", "Retest and gate", "Performance go / no-go gate", "IPL", "VP", D(2026, 12, 4), D(2026, 12, 4), M, "PPM,SME,CUT", "ECS"),
    ("5", "Phase 5  PRD readiness and hypercare", None),
    ("5.1", "PRD readiness", "PRD parity checks: HANA parameters, work processes, number ranges, IS tenant, Cloud Connector HA", "BAS", "IPL", D(2026, 12, 7), D(2026, 12, 11), T, "ECS,BTP", "PPM"),
    ("5.2", "PRD readiness", "Going-Live Check verification and ECS PRD sizing confirmation", "BAS", "IPL", D(2026, 12, 7), D(2026, 12, 11), T, "ECS", "VP"),
    ("M5a", "PRD readiness", "Tech go-live", "CUT", "VP", D(2026, 12, 15), D(2026, 12, 15), M, "IPL", "PPM"),
    ("5.3", "PRD readiness", "Non-destructive PRD smoke: connectivity, read-only checks, synthetic monitors", "PET", "IPL", D(2026, 12, 15), D(2026, 12, 23), T, "BAS,BTP,CUT", "PPM"),
    ("5.4", "PRD readiness", "Hypercare alert thresholds live, using the same KPIs", "BAS", "IPL", D(2026, 12, 14), D(2026, 12, 31), T, "BTP,PPM", "VP"),
    ("M5b", "Hypercare", "Business go-live", "CUT", "VP", D(2027, 1, 1), D(2027, 1, 1), M, "IPL", ""),
    ("5.5", "Hypercare", "Peak monitoring, first two business weeks", "BAS", "IPL", D(2027, 1, 4), D(2027, 1, 15), T, "BTP,SME,ABAP", "VP"),
    ("5.6", "Hypercare", "First month-end close: performance watch and trial balance match", "SME", "IPL", D(2027, 2, 1), D(2027, 2, 5), T, "BAS,DSC,LEG", "VP"),
    ("5.7", "Hypercare", "Lessons learned and continuous performance regression proposal", "IPL", "VP", D(2027, 2, 8), D(2027, 2, 12), T, "PPM,PET", ""),
]

ws = wb.create_sheet("Plan")
title(ws, "Performance Assurance Plan  |  Oct 5, 2026 to Feb 12, 2027", "Edit Start, End, Status, % Complete. Gantt bars are conditional formats driven by Start and End.")
ws["A3"], ws["B3"] = "Gantt start (Monday)", D(2026, 10, 5)
ws["A3"].font = F(bold=True)
body(ws, 3, 2, D(2026, 10, 5), inp=True, fmt="mmm d, yyyy")
ws["F3"] = "Today"
ws["F3"].font = F(bold=True)
ws["G3"] = "=TODAY()"
ws["G3"].number_format = "mmm d, yyyy"
cols = ["ID", "Phase", "Activity", "R", "A", "Start", "End", "Workdays", "Type", "Status", "% Complete"]
HR = 5
header(ws, HR, cols)
NWEEKS = 19
G0 = len(cols) + 1
for w in range(NWEEKS):
    c = ws.cell(row=HR, column=G0 + w, value=f"=$B$3+{7 * w}")
    c.number_format = "m/d"
    c.font = F(bold=True, color="FFFFFF", size=9)
    c.fill = fill(CH)
    c.alignment = CENTER
    ws.column_dimensions[L(G0 + w)].width = 5.2
widths(ws, [6, 16, 60, 6, 6, 11, 11, 9, 10, 12, 10])
r = HR + 1
first = r
for item in PLAN:
    if item[2] is None:
        ws.cell(row=r, column=1, value=item[0]).font = F(bold=True, color="FFFFFF")
        ws.cell(row=r, column=2, value=item[1]).font = F(bold=True, color="FFFFFF")
        for c in range(1, G0 + NWEEKS):
            ws.cell(row=r, column=c).fill = fill(ST)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        r += 1
        continue
    i, ph, task, R, A, s, e, typ = item[:8]
    z = (r % 2 == 0)
    body(ws, r, 1, i, bold=(typ == M), zebra=z)
    body(ws, r, 2, ph, zebra=z)
    body(ws, r, 3, task, bold=(typ == M), zebra=z)
    body(ws, r, 4, R, center=True, zebra=z)
    body(ws, r, 5, A, center=True, zebra=z)
    body(ws, r, 6, s, inp=True, fmt="mmm d")
    body(ws, r, 7, e, inp=True, fmt="mmm d")
    body(ws, r, 8, f"=NETWORKDAYS(F{r},G{r})", center=True, zebra=z)
    body(ws, r, 9, typ, center=True, zebra=z)
    body(ws, r, 10, "Not started", inp=True, center=True)
    body(ws, r, 11, 0, inp=True, fmt="0%", center=True)
    for w in range(NWEEKS):
        ws.cell(row=r, column=G0 + w).border = BOX
    r += 1
last = r - 1
gr = f"{L(G0)}{first}:{L(G0 + NWEEKS - 1)}{last}"
gc = L(G0)
ws.conditional_formatting.add(gr, FormulaRule(formula=[f'AND($I{first}="Milestone",$F{first}<={gc}${HR}+6,$F{first}>={gc}${HR})'], fill=fill(MA), stopIfTrue=True))
ws.conditional_formatting.add(gr, FormulaRule(formula=[f'AND($I{first}="Task",$J{first}="Complete",$F{first}<={gc}${HR}+6,$G{first}>={gc}${HR})'], fill=fill("A9B0B4"), stopIfTrue=True))
ws.conditional_formatting.add(gr, FormulaRule(formula=[f'AND($I{first}="Task",$F{first}<={gc}${HR}+6,$G{first}>={gc}${HR})'], fill=fill(OR), stopIfTrue=True))
ws.conditional_formatting.add(gr, FormulaRule(formula=[f'AND($G$3>={gc}${HR},$G$3<={gc}${HR}+6)'], fill=fill("FDE3D9")))
dv_list(ws, ["Not started", "In progress", "Complete", "At risk", "Blocked"], f"J{first}:J{last}")
ws.conditional_formatting.add(f"J{first}:J{last}", CellIsRule(operator="equal", formula=['"At risk"'], fill=fill("FFD7C9")))
ws.conditional_formatting.add(f"J{first}:J{last}", CellIsRule(operator="equal", formula=['"Blocked"'], fill=fill("F4B6B6")))
ws.freeze_panes = ws.cell(row=HR + 1, column=4)
lg = last + 2
ws.cell(row=lg, column=3, value="Legend: orange = task, maroon = milestone, grey = complete task, pale column = current week. Program dates: UAT Oct 26 to Nov 20; cutover from Nov 23; tech go-live Dec 15; business go-live Jan 1.").font = F(italic=True, color=MUTED)

# ====================================================================== RACI
ws = wb.create_sheet("RACI")
title(ws, "RACI by plan activity", "R responsible, A accountable (exactly one per row), C consulted, I informed. Role codes are explained on the Read Me tab.")
ROLE_NAMES = {"VP": "VP IT / steering", "IPL": "INTL perf lead", "PPM": "PwC perf mgr", "PET": "Perf eng team", "TDE": "Test data eng", "BAS": "Basis / HANA",
              "ECS": "SAP ECS", "BTP": "BTP integration", "ABAP": "ABAP fix team", "DSC": "DataStage / Control-M", "SME": "Functional SMEs",
              "LEG": "Legacy and SaaS owners", "SEC": "Security / GRC", "CUT": "Cutover lead"}
header(ws, 4, ["ID", "Activity"] + [f"{k}\n{ROLE_NAMES[k]}" for k in ROLES] + ["A check"])
ws.row_dimensions[4].height = 42
widths(ws, [6, 62] + [9.5] * len(ROLES) + [10])
r = 5
for item in PLAN:
    if item[2] is None or item[7] == M:
        continue
    i, ph, task, R, A, s, e, typ, Cs, Is = item
    z = (r % 2 == 0)
    body(ws, r, 1, i, zebra=z)
    body(ws, r, 2, task, zebra=z)
    Cl = [x for x in Cs.split(",") if x]
    Il = [x for x in Is.split(",") if x]
    for j, role in enumerate(ROLES):
        v = ""
        if role == A and role == R:
            v = "A"  # accountable and doing; R implied
        elif role == A:
            v = "A"
        elif role == R:
            v = "R"
        elif role in Cl:
            v = "C"
        elif role in Il:
            v = "I"
        body(ws, r, 3 + j, v, inp=False, center=True)
    lc = L(2 + len(ROLES))
    body(ws, r, 3 + len(ROLES), f'=IF(COUNTIF(C{r}:{lc}{r},"A")=1,"OK","Fix")', center=True)
    r += 1
rl = r - 1
rng = f"C5:{L(2 + len(ROLES))}{rl}"
for v, col, fc in [("A", MA, "FFFFFF"), ("R", OR, CH), ("C", CARD, CH), ("I", "F7F7F7", MUTED)]:
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{v}"'], fill=fill(col), font=Font(name="Arial", bold=True, color=fc)))
chk = f"{L(3 + len(ROLES))}5:{L(3 + len(ROLES))}{rl}"
ws.conditional_formatting.add(chk, CellIsRule(operator="equal", formula=['"Fix"'], fill=fill("F4B6B6")))
dv_list(ws, ["R", "A", "C", "I"], rng)
ws.freeze_panes = "C5"
ws.cell(row=rl + 2, column=2, value="Where the accountable role also does the work, only A is shown (A implies R).").font = F(italic=True, color=MUTED)

# ====================================================================== Scenario Catalog
ws = wb.create_sheet("Scenario Catalog")
title(ws, "Scenario catalog with risk scoring", "Score Volume, Criticality and Complexity 1 to 5. An override reason forces Tier 1. Thresholds are proposals until signed (Oct 23).")
cols = ["ID", "Value stream", "Scenario", "Entry channel", "Systems in path", "Test type", "Volume\n1-5", "Criticality\n1-5", "Complexity\n1-5",
        "Risk score", "Tier 1 override reason", "Suggested tier", "Primary KPI", "Proposed threshold", "Cycle", "Stub needed?", "Process owner", "Status"]
header(ws, 4, cols)
ws.row_dimensions[4].height = 32
widths(ws, [8, 18, 44, 16, 30, 14, 9, 10, 10, 9, 22, 11, 34, 26, 8, 10, 14, 13])
SC = [
    # OTC and billing
    ("OTC-01", "Order to cash", "VSM truck order: configure, price, tax, save", "Fiori / GUI", "S/4 VSM, AVC, pricing, OneSource", "Load", 3, 5, 5, "Revenue", "Save step response, p90", "5 s or less", "C2"),
    ("OTC-02", "Order to cash", "Order change and reconfiguration", "Fiori / GUI", "S/4 VSM, AVC, OneSource", "Load", 3, 4, 5, "", "Save step response, p90", "5 s or less", "C2"),
    ("OTC-03", "Order to cash", "Inbound dealer and legacy orders via API", "API / iFlow", "Legacy, BTP IS, S/4", "Throughput", 4, 5, 4, "", "Orders per hour, error rate", "1.5x peak, under 0.5% errors", "C1"),
    ("OTC-04", "Order to cash", "Outbound delivery and goods issue", "Fiori / GUI", "S/4 LE", "Load", 3, 4, 3, "Revenue", "Step response, p90", "2 s or less", "C2"),
    ("OTC-05", "Order to cash", "Billing run with OneSource and output", "Batch", "S/4 billing, OneSource, forms", "Throughput", 5, 5, 4, "Revenue", "Invoices per hour", "1.5x billing peak in window", "C3"),
    ("OTC-06", "Order to cash", "Invoice outbound to legacy apps", "iFlow", "S/4, BTP IS, legacy", "Throughput", 5, 4, 3, "", "Messages per hour, backlog", "1.5x peak, no backlog growth", "C1"),
    ("OTC-07", "Order to cash", "DRC Mexico CFDI to PAC and status back", "Batch / iFlow", "S/4 DRC, BTP, PAC", "Throughput", 4, 5, 4, "Regulatory", "Create to stamped, p95", "Inside SAT stamping window", "C1"),
    ("OTC-08", "Order to cash", "Cash application and customer payments", "Batch / Fiori", "S/4 FI-AR, bank", "Load", 3, 4, 4, "", "Batch runtime", "Fits window with 20% buffer", "C3"),
    # CFIN
    ("FIN-01", "Central Finance", "Infor LN JE feed at month-end peak", "JDBC", "Infor LN, DataStage, S/4 CFIN, AIF", "Throughput", 5, 5, 5, "Financial truth", "JE lines posted per hour", "1.5x month-end peak", "C1"),
    ("FIN-02", "Central Finance", "AIF error reprocessing at volume", "Fiori / GUI", "S/4 AIF", "Load", 4, 4, 4, "", "Reprocess rate", "Backlog cleared same day", "C3"),
    ("FIN-03", "Central Finance", "Trial balance match S/4 versus legacy", "Report", "S/4, Infor LN", "Load", 3, 5, 4, "Financial truth", "Report runtime; match", "30 min or less; 100% match", "C3"),
    ("FIN-04", "Financial close", "FX revaluation, depreciation, accruals", "Batch", "S/4 FI, AA", "Batch", 4, 5, 3, "", "Batch runtime", "Fits close calendar", "C3"),
    ("FIN-05", "Financial close", "Financial statements and analytical apps", "Fiori", "S/4 HANA, CDS", "Load", 3, 4, 4, "", "Analytical response, p90", "10 s or less", "C2"),
    ("FIN-06", "Financial close", "GL extracts to legacy and reporting", "Batch / file", "S/4, DataStage", "Batch", 4, 4, 3, "", "Extract runtime", "Fits window with 20% buffer", "C3"),
    ("FIN-07", "Financial close", "Period open and close steps", "Fiori / GUI", "S/4 FI", "Load", 2, 5, 3, "Financial truth", "Step response, p90", "2 s or less", "C3"),
    # P2P
    ("P2P-01", "P2P and VIM", "Ariba PO replication to S/4", "iFlow", "Ariba, BTP / CIG, S/4", "Throughput", 4, 4, 3, "", "POs per hour", "1.5x peak", "C1"),
    ("P2P-02", "P2P and VIM", "Goods receipt and service entry", "Fiori", "S/4 MM", "Load", 4, 4, 3, "", "Step response, p90", "2 s or less", "C2"),
    ("P2P-03", "P2P and VIM", "VIM OCR intake in bulk", "File / iFlow", "OpenText capture, S/4 VIM", "Throughput", 5, 4, 4, "Known pain", "Invoices to DP doc per hour", "1.5x daily peak hour", "C1"),
    ("P2P-04", "P2P and VIM", "VIM approval workflow, concurrent approvers", "Fiori", "S/4 VIM, workflow", "Load", 4, 4, 4, "Known pain", "Inbox and approve, p90", "3 s or less", "C2"),
    ("P2P-05", "P2P and VIM", "Invoice posting and 3-way match", "Batch / Fiori", "S/4 VIM, MM, FI, OneSource", "Load", 5, 4, 4, "", "Invoices posted per hour", "1.5x peak", "C2"),
    ("P2P-06", "P2P and VIM", "Payment run and bank file", "Batch", "S/4 FI-AP, bank", "Batch", 3, 5, 3, "Financial truth", "Payment run runtime", "Fits window with 20% buffer", "C3"),
    # Warranty
    ("WAR-01", "Warranty", "Pega claim inbound burst", "API / iFlow", "Pega, BTP IS, S/4", "Throughput", 4, 4, 4, "", "Claims per hour, p95 latency", "1.5x burst, 1.5 s or less", "C1"),
    ("WAR-02", "Warranty", "Claim adjudication and credit memo batch", "Batch", "S/4 warranty, FI", "Batch", 4, 4, 4, "", "Batch runtime", "Fits window with 20% buffer", "C3"),
    ("WAR-03", "Warranty", "Claim status back to Pega", "iFlow", "S/4, BTP IS, Pega", "Throughput", 4, 3, 4, "", "Messages per hour, backlog", "1.5x peak, no backlog growth", "C1"),
    # Integration and batch
    ("INT-01", "Integration and batch", "Top 20 iFlow mix at design peak", "iFlow", "BTP IS, Cloud Connector", "Throughput", 5, 4, 4, "Shared choke point", "Throughput, JMS depth", "1.5x peak, no backlog growth", "C1"),
    ("INT-02", "Integration and batch", "OneSource latency under concurrent load", "API", "S/4, OneSource", "Load", 5, 5, 3, "Shared choke point", "Tax call, p95", "800 ms or less, no timeouts", "C2"),
    ("INT-03", "Integration and batch", "Endpoint outage and backlog drain", "iFlow", "BTP IS, JMS", "Resilience", 4, 4, 4, "", "Drain time, loss", "60 min or less, zero loss", "C4"),
    ("INT-04", "Integration and batch", "Nightly Control-M critical path", "Batch", "Control-M, S/4, SOA, DataStage", "Batch", 5, 4, 4, "", "Critical path runtime", "Fits window with 20% buffer", "C3"),
    ("INT-05", "Integration and batch", "Month-end batch chain", "Batch", "Control-M, S/4, DataStage", "Batch", 5, 5, 4, "", "Chain runtime", "Fits close calendar", "C3"),
    ("INT-06", "Integration and batch", "DataStage and SOA jobs alongside online", "Mixed", "DataStage, SOA, S/4", "Load", 4, 4, 3, "", "Online p90 during batch", "Under 10% degradation", "C3"),
    # Platform
    ("PLT-01", "Platform and mixed", "Morning login storm and launchpad", "Fiori", "Web Dispatcher, IAS, S/4", "Load", 4, 4, 3, "", "Launchpad load, p90", "4 s or less", "C2"),
    ("PLT-02", "Platform and mixed", "Integrated peak hour, all streams", "Mixed", "All", "Load", 5, 5, 5, "", "All Tier 1 KPIs together", "All met at PRD-equivalent", "C2"),
    ("PLT-03", "Platform and mixed", "Eight-hour soak", "Mixed", "All", "Endurance", 4, 4, 3, "", "Degradation over 8 h", "Under 10%, no memory growth", "C4"),
    ("PLT-04", "Platform and mixed", "Stress to break point", "Mixed", "All", "Stress", 4, 4, 4, "", "Knee point", "At least 1.5x design peak", "C4"),
    ("PLT-05", "Platform and mixed", "Top heavy reports and CDS views", "Fiori / GUI", "S/4 HANA", "Load", 3, 4, 4, "", "Report response, p90", "10 s or less", "C2"),
    # Tier 2 examples
    ("T2-01", "Order to cash", "Customer master replication to legacy", "iFlow", "S/4, BTP IS, legacy", "Volume", 2, 3, 3, "", "Messages per hour", "1.5x peak", "Tier 2"),
    ("T2-02", "P2P and VIM", "Supplier master sync to Ariba", "iFlow", "S/4, BTP / CIG, Ariba", "Volume", 2, 3, 3, "", "Messages per hour", "1.5x peak", "Tier 2"),
    ("T2-03", "Central Finance", "Exchange rate load", "Batch", "S/4", "Volume", 1, 4, 2, "", "Runtime", "Fits window", "Tier 2"),
    ("T2-04", "Order to cash", "Credit management check", "Fiori / GUI", "S/4 FIN-FSCM", "Volume", 3, 3, 3, "", "Step response, p90", "2 s or less", "Tier 2"),
    ("T2-05", "Integration and batch", "Error notification and alert iFlows", "iFlow", "BTP IS", "Volume", 3, 2, 2, "", "Messages per hour", "1.5x peak", "Tier 3"),
]
r = 5
for row in SC:
    i, vs, sc, ch, sy, tt, v, c, x, ov, kpi, thr, cyc = row
    z = (r % 2 == 0)
    for j, val in enumerate([i, vs, sc, ch, sy, tt], start=1):
        body(ws, r, j, val, zebra=z)
    body(ws, r, 7, v, inp=True, center=True)
    body(ws, r, 8, c, inp=True, center=True)
    body(ws, r, 9, x, inp=True, center=True)
    body(ws, r, 10, f'=IF(COUNT(G{r}:I{r})=3,G{r}*H{r}*I{r},"")', center=True, zebra=z)
    body(ws, r, 11, ov, inp=True)
    body(ws, r, 12, f'=IF(J{r}="","",IF(OR(K{r}<>"",J{r}>=48),"Tier 1",IF(J{r}>=20,"Tier 2","Tier 3")))', center=True, bold=True, zebra=z)
    body(ws, r, 13, kpi, zebra=z)
    body(ws, r, 14, thr, inp=True)
    body(ws, r, 15, cyc, center=True, zebra=z)
    body(ws, r, 16, "Decide" if any(k in sy for k in ["OneSource", "PAC", "legacy", "Legacy", "Pega", "OpenText"]) else "No", inp=True, center=True)
    body(ws, r, 17, "", inp=True)
    body(ws, r, 18, "Draft", inp=True, center=True)
    r += 1
for k in range(5):  # blank rows for additions
    for j in range(1, 19):
        body(ws, r, j, "", inp=j in (7, 8, 9, 11, 14, 16, 17, 18))
    ws.cell(row=r, column=10, value=f'=IF(COUNT(G{r}:I{r})=3,G{r}*H{r}*I{r},"")')
    ws.cell(row=r, column=12, value=f'=IF(J{r}="","",IF(OR(K{r}<>"",J{r}>=48),"Tier 1",IF(J{r}>=20,"Tier 2","Tier 3")))')
    r += 1
scl = r - 1
ws.conditional_formatting.add(f"L5:L{scl}", CellIsRule(operator="equal", formula=['"Tier 1"'], fill=fill(OR), font=Font(name="Arial", bold=True, color=CH)))
ws.conditional_formatting.add(f"L5:L{scl}", CellIsRule(operator="equal", formula=['"Tier 2"'], fill=fill(CH), font=Font(name="Arial", bold=True, color="FFFFFF")))
ws.conditional_formatting.add(f"L5:L{scl}", CellIsRule(operator="equal", formula=['"Tier 3"'], fill=fill(ST), font=Font(name="Arial", bold=True, color="FFFFFF")))
dv_list(ws, ["Draft", "Signed", "Scripted", "Executed - pass", "Executed - fail", "Retest pass", "Waived"], f"R5:R{scl}")
dv_list(ws, ["Yes", "No", "Decide"], f"P5:P{scl}")
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"G5:I{scl}")
ws.freeze_panes = "D5"
s0 = scl + 2
ws.cell(row=s0, column=2, value="Tier 1 count").font = F(bold=True)
ws.cell(row=s0, column=3, value=f'=COUNTIF(L5:L{scl},"Tier 1")').font = F(bold=True)
ws.cell(row=s0 + 1, column=2, value="Tier 2 count").font = F(bold=True)
ws.cell(row=s0 + 1, column=3, value=f'=COUNTIF(L5:L{scl},"Tier 2")').font = F(bold=True)
ws.cell(row=s0 + 2, column=2, value="Rule").font = F(bold=True)
ws.cell(row=s0 + 2, column=3, value="Score 48 or more, or any override reason (regulatory, financial truth, known pain, revenue, shared choke point) = Tier 1. 20 to 47 = Tier 2. Below 20 = Tier 3.").font = F(italic=True, color=MUTED)

# ====================================================================== Workload Model
ws = wb.create_sheet("Workload Model")
title(ws, "Workload model: from daily volume to design load", "Yellow cells are inputs. Rows marked EXAMPLE carry illustrative values only; replace every input with mined volumes by Oct 14.")
ws["A3"] = "Design headroom (x measured peak hour)"
ws["A3"].font = F(bold=True)
body(ws, 3, 4, 1.5, inp=True, fmt="0.0x", center=True)
ws["D3"].comment = Comment("Program default: 1.5 x measured peak hour. Covers growth and variance. Change only with steering agreement.", "Perf lead")
ws["F3"] = "Capacity ratio PRD / pre-prod (from Scaling Model)"
ws["F3"].font = F(bold=True)
body(ws, 3, 10, "='Scaling Model'!C15", fmt="0.00", center=True)
cols = ["ID", "Scenario", "Volume unit", "Avg daily volume", "Peak-day multiplier", "Peak-hour share of day", "Measured peak hour",
        "Design load per hour", "Pre-prod step 1 per hour (class B)", "Pre-prod step 2 per hour (class C)", "Minutes per business transaction incl. think time",
        "Virtual users at design load", "Test hours per cycle", "Records needed (4 runs)", "Source / status"]
header(ws, 5, cols)
ws.row_dimensions[5].height = 58
widths(ws, [8, 42, 14, 12, 11, 11, 12, 12, 13, 13, 15, 12, 10, 12, 30])
EX = {"OTC-01": ("orders", 400, 1.8, 0.15, 6, 2), "FIN-01": ("JE lines", 250000, 4.0, 0.20, None, 4), "P2P-03": ("invoices", 3000, 1.5, 0.18, None, 2)}
r = 6
for row in SC[:35]:
    i, sc = row[0], row[2]
    z = (r % 2 == 0)
    body(ws, r, 1, i, zebra=z)
    body(ws, r, 2, sc, zebra=z)
    ex = EX.get(i)
    body(ws, r, 3, ex[0] if ex else "", inp=True)
    body(ws, r, 4, ex[1] if ex else None, inp=True, fmt="#,##0")
    body(ws, r, 5, ex[2] if ex else None, inp=True, fmt="0.0")
    body(ws, r, 6, ex[3] if ex else None, inp=True, fmt="0%")
    body(ws, r, 7, f'=IF(COUNT(D{r}:F{r})=3,D{r}*E{r}*F{r},"")', fmt="#,##0", zebra=z)
    body(ws, r, 8, f'=IF(G{r}="","",G{r}*$D$3)', fmt="#,##0", zebra=z, bold=True)
    body(ws, r, 9, f'=IF(H{r}="","",H{r}/$J$3)', fmt="#,##0", zebra=z)
    body(ws, r, 10, f'=IF(H{r}="","",H{r})', fmt="#,##0", zebra=z)
    body(ws, r, 11, ex[4] if ex and ex[4] else None, inp=True, fmt="0.0")
    body(ws, r, 12, f'=IF(OR(H{r}="",K{r}=""),"",ROUNDUP(H{r}*K{r}/60,0))', fmt="#,##0", zebra=z)
    body(ws, r, 13, ex[5] if ex else None, inp=True, fmt="0")
    body(ws, r, 14, f'=IF(OR(H{r}="",M{r}=""),"",H{r}*M{r}*4)', fmt="#,##0", zebra=z)
    body(ws, r, 15, "EXAMPLE values, replace" if ex else "To mine", inp=True)
    r += 1
wl = r - 1
ws.freeze_panes = "C6"
n = wl + 2
notes = [
    "Measured peak hour = daily volume x peak-day multiplier x peak-hour share. Use the busiest hour of the busiest day (month-end days 1 to 3, billing cut-off).",
    "Design load = measured peak hour x headroom. Class B (throughput) scenarios run at design / ratio in pre-prod for a PRD-equivalent result; class C (fixed limits) run at full design load.",
    "Virtual users = design load per hour x minutes per transaction / 60 (Little's Law). Leave minutes blank for non-UI flows.",
    "Records needed covers cycle run, retest and two spares at design rate. Size the synthetic data factory from this column.",
]
for k, t in enumerate(notes):
    ws.cell(row=n + k, column=2, value=t).font = F(italic=True, color=MUTED)

# ====================================================================== Scaling Model
ws = wb.create_sheet("Scaling Model")
title(ws, "Scaling model: reading a 50% pre-prod", "Enter the ECS configuration for both tiers. If not yet received, the assumed ratio (2.0, from VP IT: pre-prod is half of PRD) is used.")
header(ws, 4, ["Capacity dimension", "PRD", "Pre-prod", "Ratio PRD / pre-prod", "Notes"])
widths(ws, [42, 14, 14, 18, 60])
dims = [("Application servers (count)", "App tier"), ("Application tier vCPU (total)", "App tier"), ("Dialog work processes (total)", "App tier"),
        ("Background work processes (total)", "Batch"), ("SAPS, application tier", "App tier"), ("HANA vCPU", "DB tier"), ("HANA memory (GB)", "DB tier"),
        ("Integration Suite tenant (shared or separate?)", "Class C: same limit, do not scale")]
for k, (d, note) in enumerate(dims):
    r = 5 + k
    body(ws, r, 1, d, bold=True)
    body(ws, r, 2, None, inp=True, fmt="#,##0")
    body(ws, r, 3, None, inp=True, fmt="#,##0")
    body(ws, r, 4, f'=IFERROR(IF(AND(B{r}>0,C{r}>0),B{r}/C{r},""),"")', fmt="0.00", center=True)
    body(ws, r, 5, note)
body(ws, 13, 1, "Assumed ratio if ECS config not yet received", bold=True)
body(ws, 13, 3, 2.0, inp=True, fmt="0.00", center=True)
ws["C13"].comment = Comment("From VP IT: pre-prod is sized at half of PRD. Replace with ECS configuration when received.", "Perf lead")
body(ws, 14, 1, "Non-linearity derate for class B projections", bold=True)
body(ws, 14, 3, 0.85, inp=True, fmt="0.00", center=True)
body(ws, 15, 1, "Capacity ratio used (bottleneck tier)", bold=True)
body(ws, 15, 3, "=IF(COUNT(D5:D11)=0,C13,MIN(D5:D11))", fmt="0.00", center=True, bold=True)
body(ws, 15, 5, "Smallest measured ratio across app and DB tiers, because the bottleneck tier limits throughput.")

header(ws, 18, ["Metric class", "Scales with SAP capacity?", "Pre-prod test level", "PRD translation rule", "Examples"])
cls = [
    ("A  Response time and single-thread runtime", "No (1:1)", "Real single-user and peak pacing", "PRD forecast = pre-prod result (same CPU generation, same data volume)", "VSM configure step, single batch job, one OneSource call"),
    ("B  Throughput and concurrency", "Yes, not linearly", "50% of design, then ramp to break", "PRD capacity = measured x ratio x derate", "Concurrent users, invoices per hour, JE lines per hour"),
    ("C  Fixed shared and external limits", "No (same limit)", "100% to 150% of PRD design load", "PRD limit = pre-prod limit", "BTP tenant, JMS, EOIO, Cloud Connector, number range locks, OneSource, PAC, Pega"),
]
for k, row in enumerate(cls):
    for j, v in enumerate(row, start=1):
        body(ws, 19 + k, j, v, zebra=(k % 2 == 1), bold=(j == 1))

header(ws, 24, ["Metric (link to scenario ID)", "Class", "Measured in pre-prod", "PRD projection", "PRD design target", "Headroom", "Verdict"])
ws.column_dimensions["F"].width = 12
ws.column_dimensions["G"].width = 12
exm = [("OTC-05 Billing run, invoices per hour", "B"), ("FIN-01 JE lines posted per hour", "B"), ("P2P-03 VIM invoices per hour", "B"),
       ("INT-01 Top 20 iFlow mix, messages per hour", "C"), ("INT-02 OneSource call p95 (ms)", "A"), ("INT-04 Nightly critical path (min)", "A")]
for k, (m, c) in enumerate(exm):
    r = 25 + k
    body(ws, r, 1, m, bold=True)
    body(ws, r, 2, c, inp=True, center=True)
    body(ws, r, 3, None, inp=True, fmt="#,##0")
    body(ws, r, 4, f'=IF(C{r}="","",IF(B{r}="B",C{r}*$C$15*$C$14,C{r}))', fmt="#,##0", center=True)
    body(ws, r, 5, None, inp=True, fmt="#,##0")
    lower_better = "ms" in m or "min" in m
    if lower_better:
        body(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",E{r}/D{r})', fmt="0.00x", center=True)
    else:
        body(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",D{r}/E{r})', fmt="0.00x", center=True)
    body(ws, r, 7, f'=IF(F{r}="","",IF(F{r}>=1.2,"PASS",IF(F{r}>=1,"MARGINAL","AT RISK")))', center=True, bold=True)
ws.conditional_formatting.add("G25:G30", CellIsRule(operator="equal", formula=['"AT RISK"'], fill=fill("F4B6B6")))
ws.conditional_formatting.add("G25:G30", CellIsRule(operator="equal", formula=['"MARGINAL"'], fill=fill("FFD7C9")))
ws.conditional_formatting.add("G25:G30", CellIsRule(operator="equal", formula=['"PASS"'], fill=fill("D9EAD3")))
dv_list(ws, ["A", "B", "C"], "B25:B40")
ws.cell(row=32, column=1, value="Headroom = projection / target for throughput metrics, target / projection for time metrics. PASS at 1.2x or better, MARGINAL 1.0 to 1.2x.").font = F(italic=True, color=MUTED)

# ====================================================================== KPI Library
ws = wb.create_sheet("KPI Library")
title(ws, "KPI library: proposed defaults", "Process owners confirm per Tier 1 scenario by Oct 23. Thresholds apply at PRD-equivalent load.")
header(ws, 4, ["Class", "KPI", "Proposed threshold", "Measured with", "Notes"])
widths(ws, [20, 46, 30, 40, 50])
KP = [
    ("Online, simple", "Fiori or GUI dialog step response, 90th percentile", "2 s or less", "NeoLoad, STAD", "Excludes network latency outside RISE"),
    ("Online, complex", "VSM configure, price and save; VIM approval", "5 s or less", "NeoLoad, STAD, SAT", "Confirm with OTC and AP process owners"),
    ("Online, analytical", "Analytical Fiori apps and heavy reports, p90", "10 s or less", "NeoLoad, ST03N", "Longer runs go to background"),
    ("Online, system", "Average dialog response time, system wide", "1,000 ms or less", "ST03N", "DB time under 40% of response"),
    ("Online, launchpad", "Fiori launchpad first load, p90", "4 s or less", "NeoLoad", "Sensitive to role catalog size"),
    ("Error rate", "Failed transactions in load tests", "Under 0.5%", "NeoLoad", "Functional errors raised as defects"),
    ("Synchronous API", "OneSource tax call, p95", "800 ms or less, no timeouts", "IS monitor, STAD", "Validate against OneSource vendor SLA"),
    ("Synchronous API", "Inbound sync API via Integration Suite, p95", "1.5 s or less end to end", "IS monitor", ""),
    ("Async interfaces", "Sustained throughput versus design peak", "1.5x peak, no backlog growth", "IS monitor, JMS", ""),
    ("Resilience", "Backlog drain after 1-hour endpoint outage", "60 min or less, zero loss", "IS monitor, JMS", "Run in cycle 4"),
    ("Central Finance", "JE lines posted per hour", "1.5x month-end peak", "AIF monitor, DataStage logs", ""),
    ("Central Finance", "Trial balance S/4 versus legacy", "100% match; report 30 min or less", "Recon report", "Financial truth, Tier 1 override"),
    ("DRC Mexico", "eDocument create to PAC stamped, p95", "Inside SAT stamping window with margin", "eDocument Cockpit", "Confirm window with tax"),
    ("VIM", "OCR intake to DP document available", "Within agreed minutes at peak", "VIM analytics", "Known pain point"),
    ("Batch", "Critical path versus batch window", "Fits with 20% buffer", "Control-M, SM37", "Per window: nightly, month-end"),
    ("Batch", "Single job runtime versus Mock-2 baseline", "No more than 1.2x baseline", "SM37, Control-M", ""),
    ("Platform", "App server and HANA CPU, sustained", "70% or less at PRD-equivalent", "HANA Cockpit, OS monitor", ""),
    ("Platform", "HANA memory used versus allocation limit", "80% or less, no OOM", "HANA Cockpit", ""),
    ("Platform", "Free dialog work processes", "20% or more free", "SM66, ST03N", ""),
    ("Platform", "Update queue and enqueue waits", "No backlog; enqueue wait near zero", "SM13, SM12", ""),
    ("Platform", "Short dumps during test", "No new TIME_OUT or memory dumps", "ST22", ""),
    ("Endurance", "Degradation over 8 hours", "Under 10%, no memory growth", "NeoLoad, HANA Cockpit", "Run in cycle 4"),
]
for k, row in enumerate(KP):
    for j, v in enumerate(row, start=1):
        body(ws, 5 + k, j, v, inp=(j == 3), zebra=(k % 2 == 1) and j != 3, bold=(j == 1))

# ====================================================================== Interface Inventory
ws = wb.create_sheet("Interface Inventory")
title(ws, "Interface inventory (168 BTP interfaces)", "Fill one row per interface. Risk score and suggested tier are calculated. Row EX shows the expected format.")
cols = ["ID", "Interface name", "Source", "Target", "Middleware", "Pattern", "QoS", "Frequency", "Avg messages per day", "Peak messages per hour",
        "Avg payload KB", "Max payload KB", "Volume 1-5", "Criticality 1-5", "Complexity 1-5", "Risk score", "Suggested tier", "Test approach", "Stub needed?", "Owner"]
header(ws, 4, cols)
ws.row_dimensions[4].height = 32
widths(ws, [8, 34, 14, 14, 14, 12, 9, 12, 12, 12, 10, 10, 9, 10, 10, 9, 11, 26, 10, 14])
ex = ["EX", "Billing invoice outbound to dealer system", "S/4HANA", "Legacy dealer app", "BTP IS", "Async", "EO", "Near real time", 8000, 1200, 12, 250, 5, 4, 3]
for j, v in enumerate(ex, start=1):
    c = body(ws, 5, j, v, fmt="#,##0" if isinstance(v, int) and j > 8 else None)
    c.font = F(italic=True, color=MUTED)
body(ws, 5, 16, "=M5*N5*O5", center=True).font = F(italic=True, color=MUTED)
body(ws, 5, 17, '=IF(M5*N5*O5>=48,"Tier 1",IF(M5*N5*O5>=20,"Tier 2","Tier 3"))', center=True).font = F(italic=True, color=MUTED)
body(ws, 5, 18, "Tier 1 scenario OTC-06").font = F(italic=True, color=MUTED)
body(ws, 5, 19, "Decide").font = F(italic=True, color=MUTED)
body(ws, 5, 20, "BTP team").font = F(italic=True, color=MUTED)
for k in range(168):
    r = 6 + k
    body(ws, r, 1, f"INT-{k + 1:03d}")
    for j in range(2, 16):
        body(ws, r, j, None, inp=True, fmt="#,##0" if 9 <= j <= 12 else None, center=j >= 13)
    body(ws, r, 16, f'=IF(COUNT(M{r}:O{r})=3,M{r}*N{r}*O{r},"")', center=True)
    body(ws, r, 17, f'=IF(P{r}="","",IF(P{r}>=48,"Tier 1",IF(P{r}>=20,"Tier 2","Tier 3")))', center=True, bold=True)
    for j in (18, 19, 20):
        body(ws, r, j, None, inp=True)
il = 6 + 167
dv_list(ws, ["BTP IS", "CIG", "SOA", "DataStage", "Direct RFC", "File / SFTP", "Other"], f"E6:E{il}")
dv_list(ws, ["Sync", "Async", "Batch file", "Event"], f"F6:F{il}")
dv_list(ws, ["BE", "EO", "EOIO", "n/a"], f"G6:G{il}")
dv_list(ws, ["Yes", "No", "Decide"], f"S6:S{il}")
dv2 = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
ws.add_data_validation(dv2)
dv2.add(f"M6:O{il}")
for t, col, fc in [("Tier 1", OR, CH), ("Tier 2", CH, "FFFFFF"), ("Tier 3", ST, "FFFFFF")]:
    ws.conditional_formatting.add(f"Q6:Q{il}", CellIsRule(operator="equal", formula=[f'"{t}"'], fill=fill(col), font=Font(name="Arial", bold=True, color=fc)))
ws.freeze_panes = "C6"

# ====================================================================== Batch Inventory
ws = wb.create_sheet("Batch Inventory")
title(ws, "Batch inventory (Control-M, SAP, DataStage, SOA)", "Critical-path jobs first. Mock-2 runtime is the baseline. Buffer is calculated against the window.")
cols = ["ID", "Job or chain", "Scheduler", "System", "Frequency", "Window start", "Window end", "Window minutes", "Mock-2 runtime (min)",
        "Pre-prod runtime (min)", "Critical path?", "Predecessors", "Buffer vs window", "Verdict", "Owner"]
header(ws, 4, cols)
ws.row_dimensions[4].height = 32
widths(ws, [8, 36, 12, 14, 12, 10, 10, 10, 12, 12, 10, 22, 11, 11, 14])
for k in range(80):
    r = 5 + k
    body(ws, r, 1, f"JOB-{k + 1:03d}")
    for j in range(2, 13):
        body(ws, r, j, None, inp=True, fmt="hh:mm" if j in (6, 7) else ("#,##0" if j in (9, 10) else None))
    body(ws, r, 8, f'=IF(OR(F{r}="",G{r}=""),"",ROUND(MOD(G{r}-F{r},1)*1440,0))', center=True)
    body(ws, r, 13, f'=IF(OR(H{r}="",J{r}=""),"",1-J{r}/H{r})', fmt="0%", center=True)
    body(ws, r, 14, f'=IF(M{r}="","",IF(M{r}>=0.2,"PASS",IF(M{r}>=0,"MARGINAL","FAIL")))', center=True, bold=True)
    body(ws, r, 15, None, inp=True)
bl = 5 + 79
dv_list(ws, ["Control-M", "SAP SM36", "DataStage", "SOA", "Other"], f"C5:C{bl}")
dv_list(ws, ["Y", "N"], f"K5:K{bl}")
ws.conditional_formatting.add(f"N5:N{bl}", CellIsRule(operator="equal", formula=['"FAIL"'], fill=fill("F4B6B6")))
ws.conditional_formatting.add(f"N5:N{bl}", CellIsRule(operator="equal", formula=['"MARGINAL"'], fill=fill("FFD7C9")))
ws.conditional_formatting.add(f"N5:N{bl}", CellIsRule(operator="equal", formula=['"PASS"'], fill=fill("D9EAD3")))
ws.freeze_panes = "C5"

# ====================================================================== Env Readiness
ws = wb.create_sheet("Env Readiness")
title(ws, "Pre-prod entry checklist (target: all green by Nov 2)", "Status drives the readiness count at the bottom.")
header(ws, 4, ["#", "Area", "Item", "Owner", "Due", "Status", "Evidence / notes"])
widths(ws, [5, 18, 70, 8, 11, 13, 40])
ER = [
    ("Data", "Pre-prod refreshed with Mock-converted data", "BAS", D(2026, 10, 30)),
    ("Data", "Table sizes checked against PRD projection (ACDOCA, VBAK/VBRK, VIM, AIF)", "BAS", D(2026, 10, 30)),
    ("Data", "Synthetic data pools loaded for cycles 1 to 4 plus retest", "TDE", D(2026, 11, 2)),
    ("Config", "Transport and configuration parity with PRD confirmed", "BAS", D(2026, 10, 30)),
    ("Config", "HANA parameters match PRD", "BAS", D(2026, 10, 30)),
    ("Config", "Work process layout and operation modes match PRD", "BAS", D(2026, 10, 30)),
    ("Config", "Number range buffering matches PRD design (FI, billing, eDocument)", "BAS", D(2026, 10, 30)),
    ("Config", "ECS configuration sheet for pre-prod and PRD on file", "ECS", D(2026, 10, 16)),
    ("Integration", "Integration Suite test tenant configured like PRD (JMS, retries, timeouts)", "BTP", D(2026, 10, 30)),
    ("Integration", "Cloud Connector set up like PRD (HA where PRD is HA)", "BTP", D(2026, 10, 30)),
    ("Integration", "Stubs live for endpoints that cannot take load", "BTP", D(2026, 10, 30)),
    ("Integration", "Real endpoints confirmed for scenarios that use them, with agreed load windows", "LEG", D(2026, 10, 30)),
    ("Integration", "DataStage JDBC path to CFIN staging working in pre-prod", "DSC", D(2026, 10, 30)),
    ("Integration", "Control-M connected to pre-prod with replay schedule loaded", "DSC", D(2026, 11, 4)),
    ("Security", "Performance users created from production business roles (no SAP_ALL)", "SEC", D(2026, 10, 30)),
    ("Security", "Communication users with production-like authorizations", "SEC", D(2026, 10, 30)),
    ("Security", "Authentication approach for scripted users agreed (SSO / IAS)", "SEC", D(2026, 10, 23)),
    ("Tooling", "NeoLoad controller and generators reach RISE pre-prod", "PET", D(2026, 10, 23)),
    ("Tooling", "Tier 1 scripts pass single-user validation", "PET", D(2026, 11, 2)),
    ("Monitoring", "ST03N, STAD and SQLM retention extended", "BAS", D(2026, 10, 30)),
    ("Monitoring", "HANA Cockpit, IS monitor and Cloud ALM dashboards ready", "BAS", D(2026, 10, 30)),
    ("Monitoring", "Results template and PRD forecast sheet ready", "PPM", D(2026, 10, 30)),
    ("Operations", "Snapshot before cycle 1 taken; restore tested", "ECS", D(2026, 11, 2)),
    ("Operations", "Pre-prod slot calendar agreed with cutover lead", "IPL", D(2026, 10, 9)),
    ("Operations", "Defect workflow and priority transport lane for performance fixes", "PPM", D(2026, 10, 30)),
    ("Governance", "KPIs signed by process owners", "PPM", D(2026, 10, 23)),
    ("Governance", "Calibration run complete; scaling ratio confirmed", "PET", D(2026, 11, 3)),
]
for k, (a, it, o, d) in enumerate(ER):
    r = 5 + k
    z = (k % 2 == 1)
    body(ws, r, 1, k + 1, center=True, zebra=z)
    body(ws, r, 2, a, zebra=z, bold=True)
    body(ws, r, 3, it, zebra=z)
    body(ws, r, 4, o, center=True, zebra=z)
    body(ws, r, 5, d, inp=True, fmt="mmm d", center=True)
    body(ws, r, 6, "Open", inp=True, center=True)
    body(ws, r, 7, None, inp=True)
el = 4 + len(ER)
dv_list(ws, ["Open", "In progress", "Done", "Blocked", "N/A"], f"F5:F{el}")
ws.conditional_formatting.add(f"F5:F{el}", CellIsRule(operator="equal", formula=['"Done"'], fill=fill("D9EAD3")))
ws.conditional_formatting.add(f"F5:F{el}", CellIsRule(operator="equal", formula=['"Blocked"'], fill=fill("F4B6B6")))
ws.cell(row=el + 2, column=2, value="Done").font = F(bold=True)
ws.cell(row=el + 2, column=3, value=f'=COUNTIF(F5:F{el},"Done")&" of "&(COUNTA(F5:F{el})-COUNTIF(F5:F{el},"N/A"))&" items complete"').font = F(bold=True)

# ====================================================================== Risks and Decisions
ws = wb.create_sheet("Risks and Decisions")
title(ws, "Risk log and decision log", "Score = likelihood x impact (1 to 5 each). 15 or more = High, 8 to 14 = Medium.")
header(ws, 4, ["ID", "Risk", "Likelihood", "Impact", "Score", "Rating", "Mitigation", "Owner", "Review date", "Status"])
widths(ws, [7, 46, 10, 9, 8, 10, 62, 8, 12, 12])
RK = [
    ("Pre-prod contention with cutover rehearsal and UAT", 4, 5, "Reserve Nov 2 to Dec 4 now; slot nights and weekends; PRD window as contingency", "IPL"),
    ("Team pulled into SIT2 and Mock-2 firefighting", 5, 4, "Dedicated external performance team; SMEs ring-fenced at 25%", "VP"),
    ("Volumes unknown today", 5, 3, "Mine legacy data in week 1; 1.5x headroom flagged as assumption", "TDE"),
    ("Legacy and SaaS endpoints cannot take load", 4, 4, "Stub with mock iFlows; separate low-rate contract test against the real endpoint", "LEG"),
    ("Fixes arrive too late to retest", 4, 5, "Shift-left in SIT2; twice-weekly triage; priority transport lane", "PPM"),
    ("Pre-prod data not production-shaped", 3, 4, "Refresh from Mock load; check table sizes against PRD projection", "BAS"),
    ("Scaling misread leads to false confidence", 3, 4, "Three-class model, ECS config sheet, calibration run, class C at full load", "IPL"),
    ("SSO blocks scripted performance users", 3, 3, "Agree authentication approach for performance users in week 2", "SEC"),
    ("Performance defect cannot be fixed by Dec 15", 3, 5, "Pre-agreed workarounds (scheduling, parallelization) and hypercare alerts", "IPL"),
    ("OneSource or PAC vendor limits unknown", 3, 4, "Request vendor rate limits and SLAs in week 1; design retries and timeouts", "BTP"),
    ("Number range serialization on Mexico documents", 2, 5, "Verify buffering design in SIT2; test billing and DRC at full design load", "BAS"),
]
for k, (rk, li, im, mi, ow) in enumerate(RK):
    r = 5 + k
    z = (k % 2 == 1)
    body(ws, r, 1, f"R{k + 1:02d}", zebra=z)
    body(ws, r, 2, rk, zebra=z)
    body(ws, r, 3, li, inp=True, center=True)
    body(ws, r, 4, im, inp=True, center=True)
    body(ws, r, 5, f"=C{r}*D{r}", center=True, zebra=z)
    body(ws, r, 6, f'=IF(E{r}>=15,"High",IF(E{r}>=8,"Medium","Low"))', center=True, bold=True, zebra=z)
    body(ws, r, 7, mi, zebra=z)
    body(ws, r, 8, ow, center=True, zebra=z)
    body(ws, r, 9, D(2026, 10, 9), inp=True, fmt="mmm d", center=True)
    body(ws, r, 10, "Open", inp=True, center=True)
rl2 = 4 + len(RK)
ws.conditional_formatting.add(f"F5:F{rl2}", CellIsRule(operator="equal", formula=['"High"'], fill=fill(MA), font=Font(name="Arial", bold=True, color="FFFFFF")))
ws.conditional_formatting.add(f"F5:F{rl2}", CellIsRule(operator="equal", formula=['"Medium"'], fill=fill(OR), font=Font(name="Arial", bold=True, color=CH)))
dv_list(ws, ["Open", "Mitigating", "Closed", "Realized"], f"J5:J{rl2}")

d0 = rl2 + 3
ws.cell(row=d0 - 1, column=1, value="Decision log").font = F(size=13, bold=True)
header(ws, d0, ["ID", "Decision", "Options", "", "", "", "Recommendation", "Decider", "Needed by", "Status"])
ws.merge_cells(start_row=d0, start_column=3, end_row=d0, end_column=6)
DC = [
    ("Stand up performance assurance as a funded workstream", "Fund now / absorb in existing teams / defer", "Fund now with a named International owner and PwC CR", "VP", D(2026, 10, 9)),
    ("Specialist performance team", "External partner / offshore / internal only", "External specialists (about 6) so SIT2 and UAT are not drained", "VP", D(2026, 10, 9)),
    ("Pre-prod reservation Nov 2 to Dec 4", "Exclusive / time-sliced with cutover / none", "Time-sliced with agreed slots, nights and weekends", "VP", D(2026, 10, 9)),
    ("Endpoint strategy per legacy and SaaS system", "Real instance / stub / hybrid", "Hybrid: stub for load, real endpoint for low-rate contract test", "IPL", D(2026, 10, 16)),
    ("Performance gate as input to tech go-live", "Formal gate / advisory", "Formal gate on Dec 4", "VP", D(2026, 10, 9)),
    ("PRD window before cutover (option C)", "Use / do not use", "Hold as contingency; decide by Nov 20 based on pre-prod results", "VP", D(2026, 11, 20)),
    ("Load tool", "Keep NeoLoad / switch", "Keep NeoLoad for this go-live; revisit after hypercare", "IPL", D(2026, 10, 9)),
]
for k, (dc, op, rec, who, by) in enumerate(DC):
    r = d0 + 1 + k
    z = (k % 2 == 1)
    body(ws, r, 1, f"D{k + 1:02d}", zebra=z)
    body(ws, r, 2, dc, zebra=z, bold=True)
    body(ws, r, 3, op, zebra=z)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
    body(ws, r, 7, rec, zebra=z)
    body(ws, r, 8, who, center=True, zebra=z)
    body(ws, r, 9, by, inp=True, fmt="mmm d", center=True)
    body(ws, r, 10, "Pending", inp=True, center=True)
dv_list(ws, ["Pending", "Approved", "Rejected", "Deferred"], f"J{d0 + 1}:J{d0 + len(DC)}")

# ====================================================================== Team
ws = wb.create_sheet("Team")
title(ws, "Team, FTE and duration", "FTE-weeks drive the change request. Name each person once confirmed.")
header(ws, 4, ["Role", "Code", "Source", "FTE", "Start", "End", "Weeks", "FTE-weeks", "Named person"])
widths(ws, [52, 7, 30, 7, 11, 11, 8, 10, 24])
TM = [
    ("International performance test lead (owner)", "IPL", "International", 1.0, D(2026, 10, 5), D(2027, 2, 12)),
    ("PwC performance test manager", "PPM", "PwC", 1.0, D(2026, 10, 5), D(2026, 12, 23)),
    ("Performance engineers (NeoLoad scripting and execution)", "PET", "Specialist partner or offshore", 4.0, D(2026, 10, 12), D(2026, 12, 23)),
    ("Test data engineer (synthetic data factory)", "TDE", "PwC or partner", 1.0, D(2026, 10, 7), D(2026, 12, 4)),
    ("Basis and HANA performance engineer", "BAS", "International or PwC, plus ECS", 1.0, D(2026, 10, 5), D(2027, 1, 15)),
    ("ABAP performance developers (fix team)", "ABAP", "PwC", 2.0, D(2026, 10, 12), D(2026, 12, 11)),
    ("BTP Integration Suite engineer", "BTP", "Integration team", 1.0, D(2026, 10, 12), D(2026, 12, 23)),
    ("DataStage and Control-M engineer", "DSC", "International", 0.5, D(2026, 10, 12), D(2026, 12, 4)),
    ("Functional SMEs: OTC/VSM, CFIN, P2P/VIM, warranty, tax (5 x 25%)", "SME", "Ring-fenced from program", 1.25, D(2026, 10, 12), D(2026, 12, 4)),
    ("Security and GRC", "SEC", "International", 0.25, D(2026, 10, 19), D(2026, 11, 6)),
]
for k, (role, code, src, fte, s, e) in enumerate(TM):
    r = 5 + k
    z = (k % 2 == 1)
    body(ws, r, 1, role, zebra=z, bold=True)
    body(ws, r, 2, code, center=True, zebra=z)
    body(ws, r, 3, src, zebra=z)
    body(ws, r, 4, fte, inp=True, fmt="0.00", center=True)
    body(ws, r, 5, s, inp=True, fmt="mmm d", center=True)
    body(ws, r, 6, e, inp=True, fmt="mmm d", center=True)
    body(ws, r, 7, f"=ROUND((F{r}-E{r}+1)/7,1)", fmt="0.0", center=True, zebra=z)
    body(ws, r, 8, f"=D{r}*G{r}", fmt="0.0", center=True, zebra=z)
    body(ws, r, 9, None, inp=True)
tl = 4 + len(TM)
body(ws, tl + 1, 1, "Total", bold=True)
body(ws, tl + 1, 4, f"=SUM(D5:D{tl})", fmt="0.00", center=True, bold=True)
body(ws, tl + 1, 8, f"=SUM(H5:H{tl})", fmt="0.0", center=True, bold=True)
ws.cell(row=tl + 3, column=1, value="Legacy and SaaS owners (Infor LN, Pega, OneSource, Mexico PAC, OpenText, Ariba) are named contacts, not FTE. SAP ECS and SAP Enterprise Support engage through tickets and service sessions.").font = F(italic=True, color=MUTED)

for s in wb.worksheets:
    s.sheet_properties.tabColor = {"Read Me": CH, "Plan": OR, "RACI": OR}.get(s.title, ST)
    s.page_setup.orientation = "landscape"
    s.page_setup.fitToWidth = 1
    s.sheet_properties.pageSetUpPr.fitToPage = True
    s.page_setup.fitToHeight = 0

wb.save(OUT)
print("saved", OUT)
