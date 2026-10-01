#!/usr/bin/env python3
"""Generate the NorthStar performance-strategy SVG graphics.

Each graphic is produced twice: a standalone version with its own title (for sharing),
and a 'deck' version without the header (the slide carries the title).
"""
import datetime as dt
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "svg"
os.makedirs(OUT, exist_ok=True)

CH, OR, MA, BL, ST = "#272623", "#FF7144", "#5C1916", "#0062A2", "#4E5659"
CARD, BODY, MUTED, NOTE, NOTEB, ZEB = "#E8E9EB", "#333B42", "#82817D", "#EEF2F7", "#C9D3E0", "#EAF1F4"
FONT = "Arial, Helvetica, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, color=CH, weight="normal", anchor="start", style=""):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {style}>{esc(s)}</text>')


def lines(x, y, rows, size=14, color=CH, weight="normal", anchor="start", lh=None):
    lh = lh or size * 1.3
    return "".join(text(x, y + i * lh, r, size, color, weight, anchor) for i, r in enumerate(rows))


def rect(x, y, w, h, fill=CARD, rx=8, stroke="none", sw=0, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'


def badge(cx, cy, n, fill=OR, r=14, size=15):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            + text(cx, cy + size * 0.36, str(n), size, "#FFFFFF", "bold", "middle"))


def line(x1, y1, x2, y2, color=CH, w=1.5, dash=None, arrow=True, both=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arr)"' if arrow else ""
    if both:
        m += ' marker-start="url(#arrs)"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}{m}/>'


DEFS = (f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{CH}"/></marker>'
        f'<marker id="arrs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{CH}"/></marker>'
        f'<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="8" height="8" fill="{CARD}"/><line x1="0" y1="0" x2="0" y2="8" stroke="#BAB9B5" stroke-width="3"/></pattern></defs>')


def svg(w, h, body, title=None, subtitle=None, deck=False):
    head = ""
    off = 0
    if not deck and title:
        off = 90
        head = (rect(0, 0, w, 8, OR, 0) + text(40, 50, title.upper(), 26, CH, "bold")
                + (text(40, 76, subtitle, 15, MUTED) if subtitle else ""))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h + off}" viewBox="0 0 {w} {h + off}">'
            f'<title>{esc(title or "")}</title>{DEFS}<rect width="{w}" height="{h + off}" fill="#FFFFFF"/>{head}'
            f'<g transform="translate(0,{off})">{body}</g></svg>')


# ------------------------------------------------------------------ 1. Architecture
def architecture():
    b = []
    # Left: load injection panel
    b.append(rect(20, 20, 280, 690, NOTE, 12, NOTEB, 1))
    b.append(text(40, 52, "LOAD INJECTION", 15, CH, "bold"))
    b.append(text(40, 72, "NeoLoad controller + generators", 12.5, BODY))
    b.append(text(40, 89, "in cloud network peered to RISE", 12.5, BODY))
    inj = [
        ("Online users", ["Fiori apps and SAP GUI", "through Web Dispatcher", "(perf users, near-prod roles)"]),
        ("API / iFlow injectors", ["Inbound payloads into", "Integration Suite (Pega,", "Ariba, legacy, VIM)"]),
        ("JDBC / file replay", ["Synthetic Infor LN JEs", "through DataStage into", "CFIN staging"]),
        ("Batch schedule replay", ["Control-M critical path:", "SAP, SOA and DataStage", "jobs on the real calendar"]),
    ]
    for i, (h, rows) in enumerate(inj):
        y = 115 + i * 148
        b.append(rect(36, y, 248, 132, "#FFFFFF", 10, NOTEB, 1))
        b.append(badge(62, y + 28, i + 1, OR))
        b.append(text(86, y + 33, h, 15, CH, "bold"))
        b.append(lines(52, y + 62, rows, 13, BODY))

    # Center: S/4HANA
    b.append(rect(330, 20, 590, 690, CH, 12))
    b.append(text(350, 50, "S/4HANA 2023 FPS02  |  RISE private cloud PRE-PROD", 15, "#FFFFFF", "bold"))
    b.append(text(350, 70, "Sized at about 50% of PRD, loaded with full Mock data volumes", 12.5, "#BAB9B5"))
    b.append(rect(350, 88, 550, 46, ST, 8))
    b.append(text(625, 116, "Web Dispatcher  |  Fiori Launchpad  |  SAP GUI  |  OData", 14, "#FFFFFF", "bold", "middle"))
    b.append(badge(350, 88, 1, OR, 15))
    mods = [
        ("OTC  |  VSM / AVC truck config", "Pricing, ATP, OneSource tax call", MA),
        ("Billing and output", "Invoices to legacy, forms, tax", MA),
        ("Central Finance", "AIF posting of Infor LN JEs", BL),
        ("Financial close", "Trial balance match to legacy", BL),
        ("P2P  |  VIM invoices", "OCR intake, DP docs, workflow", ST),
        ("Warranty claims", "Pega inbound, credit memos", ST),
        ("DRC eDocument (Mexico)", "CFDI to PAC, status back", MA),
        ("Background jobs", "Update tasks, bgRFC, queues", ST),
    ]
    for i, (h, s, c) in enumerate(mods):
        col, row = i % 2, i // 2
        x, y = 350 + col * 280, 150 + row * 108
        b.append(rect(x, y, 270, 94, c, 8))
        b.append(text(x + 14, y + 36, h, 14.5, "#FFFFFF", "bold"))
        b.append(text(x + 14, y + 62, s, 12.5, "#FFFFFF"))
    b.append(rect(350, 590, 550, 100, "#3A3935", 8, "#82817D", 1))
    b.append(text(625, 626, "SAP HANA database", 16, "#FFFFFF", "bold", "middle"))
    b.append(text(625, 652, "Production-like table sizes (ACDOCA, VBAK/VBRK, VIM, AIF)", 12.5, "#BAB9B5", "normal", "middle"))
    b.append(text(625, 672, "Number range buffering, memory limits, expensive SQL", 12.5, "#BAB9B5", "normal", "middle"))

    # BTP column
    b.append(rect(960, 20, 250, 450, BL, 12))
    b.append(text(1085, 52, "SAP BTP", 15, "#FFFFFF", "bold", "middle"))
    b.append(text(1085, 74, "Integration Suite", 15, "#FFFFFF", "bold", "middle"))
    b.append(badge(960, 20, 2, OR, 15))
    for i, s in enumerate(["168 interfaces (iFlows)", "JMS queues, EO / EOIO", "Retries and error storms", "Tenant message limits", "Large payload memory", "Adobe Forms service (if used)"]):
        b.append(rect(978, 96 + i * 52, 214, 40, "#FFFFFF", 6))
        b.append(text(1085, 121 + i * 52, s, 12.5, CH, "bold", "middle"))
    b.append(rect(960, 490, 250, 70, ST, 10))
    b.append(text(1085, 520, "Cloud Connector", 14.5, "#FFFFFF", "bold", "middle"))
    b.append(text(1085, 541, "HA pair and throughput", 12.5, "#FFFFFF", "normal", "middle"))
    b.append(rect(960, 580, 250, 130, OR, 10))
    b.append(badge(960, 580, 3, CH, 15))
    b.append(text(1085, 612, "IBM DataStage + Control-M", 14.5, CH, "bold", "middle"))
    b.append(lines(1085, 636, ["JDBC into CFIN staging", "Commit size, parallel streams", "Job chains and calendars"], 12.5, CH, "normal", "middle"))
    b.append(badge(1210, 580, 4, CH, 15))

    # Flows S/4 <-> BTP and DataStage
    b.append(line(922, 240, 958, 240, CH, 2.5))
    b.append(line(958, 280, 922, 280, CH, 2.5))
    b.append(line(958, 640, 922, 640, CH, 2.5))

    # Right: external systems
    ext = [
        ("Pega warranty", "API bursts, Pega throttling", False),
        ("SAP Ariba (indirect P2P)", "PO, invoice, status", False),
        ("OneSource indirect tax", "Synchronous, per line item", True),
        ("Mexico PAC / SAT", "CFDI stamping latency", True),
        ("OpenText capture (VIM)", "OCR throughput", True),
        ("Legacy invoice receivers", "Outbound invoices", True),
        ("SOA services", "Legacy middleware", True),
    ]
    for i, (h, s, stub) in enumerate(ext):
        y = 20 + i * 66
        if stub:
            b.append(rect(1250, y, 330, 56, "#FFFFFF", 8, OR, 2, "7 5"))
        else:
            b.append(rect(1250, y, 330, 56, CARD, 8))
        b.append(text(1266, y + 24, h, 14, CH, "bold"))
        b.append(text(1266, y + 44, s, 12.5, BODY))
        b.append(line(1212, y + 28, 1248, y + 28, CH, 1.5, both=True))
    # Infor LN source to DataStage
    b.append(rect(1250, 600, 330, 70, MA, 8))
    b.append(text(1266, 630, "Baan / Infor LN (legacy ERP)", 14, "#FFFFFF", "bold"))
    b.append(text(1266, 652, "Journal entries for CFIN, TB source", 12.5, "#FFFFFF"))
    b.append(line(1248, 635, 1212, 635, CH, 2.5))
    # SOA (last ext, y=416) also hooks to Control-M: leave with a dashed connector
    b.append(text(1266, 500, "SOA and legacy batch extracts are", 12.5, MUTED))
    b.append(text(1266, 518, "scheduled by Control-M (injection point 4)", 12.5, MUTED))

    # Observability band
    b.append(rect(20, 740, 1560, 130, NOTE, 12, NOTEB, 1))
    b.append(text(40, 770, "MEASURE EVERYTHING ON THE SAME CLOCK", 15, CH, "bold"))
    obs = ["ST03N, STAD, SQLM, SAT", "HANA Cockpit, plan cache", "IS message and JMS monitor",
           "AIF, eDocument Cockpit, VIM", "Cloud ALM / Focused Run", "NeoLoad analytics"]
    for i, s in enumerate(obs):
        x = 40 + i * 214
        b.append(rect(x, 788, 202, 60, "#FFFFFF", 8, NOTEB, 1))
        b.append(text(x + 101, 823, s, 12.5, CH, "bold", "middle"))
    b.append(line(1330, 818, 1362, 818, CH, 2))
    b.append(rect(1366, 788, 198, 60, OR, 8))
    b.append(text(1465, 814, "AI results triage", 14, CH, "bold", "middle"))
    b.append(text(1465, 834, "anomalies to code owners", 12, CH, "normal", "middle"))
    # Legend row
    b.append(rect(20, 890, 34, 20, CARD, 4))
    b.append(text(62, 905, "Real test instance expected", 13, BODY))
    b.append(rect(300, 890, 34, 20, "#FFFFFF", 4, OR, 2, "5 4"))
    b.append(text(342, 905, "Capacity unknown: scale it or stub it (decision by Oct 16)", 13, BODY))
    b.append(badge(780, 900, "#", OR, 11, 12))
    b.append(text(798, 905, "Injection point, matches the load injection panel", 13, BODY))
    return 1600, 920, b


# ------------------------------------------------------------------ 2. Timeline
START = dt.date(2026, 10, 5)
X0, WK = 330, 72.0
NW = 19  # weeks Oct 5 .. Feb 14


def dx(d):
    return X0 + (d - START).days / 7.0 * WK


def timeline():
    b = []
    D = dt.date
    top = 20
    # month header
    months = [(D(2026, 10, 5), "OCT 2026"), (D(2026, 11, 1), "NOV"), (D(2026, 12, 1), "DEC"), (D(2027, 1, 1), "JAN 2027"), (D(2027, 2, 1), "FEB")]
    end = START + dt.timedelta(weeks=NW)
    for i, (d, lab) in enumerate(months):
        nx = dx(months[i + 1][0]) if i + 1 < len(months) else dx(end)
        b.append(rect(dx(d), top, nx - dx(d) - 2, 30, CH, 0))
        b.append(text(dx(d) + 8, top + 20, lab, 13, "#FFFFFF", "bold"))
    for w in range(NW):
        d = START + dt.timedelta(weeks=w)
        x = X0 + w * WK
        b.append(rect(x, top + 32, WK - 2, 24, ZEB if w % 2 else "#FFFFFF", 0))
        b.append(text(x + WK / 2, top + 49, f"{d.month}/{d.day}", 11.5, MUTED, "normal", "middle"))
    gridtop, gridbot = top + 58, 690
    for w in range(NW + 1):
        x = X0 + w * WK
        b.append(f'<line x1="{x}" y1="{gridtop}" x2="{x}" y2="{gridbot}" stroke="#E0E0E0" stroke-width="1"/>')
    # protected window band
    b.append(rect(dx(D(2026, 11, 2)), gridtop, dx(D(2026, 12, 5)) - dx(D(2026, 11, 2)), gridbot - gridtop, OR, 0, opacity=0.10))

    def section(y, lab):
        b.append(text(20, y, lab, 13, MUTED, "bold"))

    def bar(y, s, e, lab, fill, tcol="#FFFFFF", hatch=False, inside=None):
        if inside is None:
            inside = (dx(e + dt.timedelta(days=1)) - dx(s)) > len(lab) * 7.6 + 16
        x1, x2 = dx(s), dx(e + dt.timedelta(days=1))
        b.append(rect(x1, y, max(x2 - x1, 6), 30, "url(#hatch)" if hatch else fill, 6))
        if inside:
            b.append(text(x1 + 10, y + 20, lab, 12.5, tcol, "bold"))
        else:
            b.append(text(x2 + 8, y + 20, lab, 12.5, CH, "bold"))

    def label(y, s):
        b.append(text(20, y + 20, s, 13.5, CH, "bold"))

    def milestone(y, d, lab, fill=CH, right=True):
        x = dx(d)
        b.append(f'<path d="M{x},{y} L{x + 11},{y + 15} L{x},{y + 30} L{x - 11},{y + 15} z" fill="{fill}"/>')
        b.append(text(x + 16 if right else x - 16, y + 20, lab, 12.5, CH, "bold", "start" if right else "end"))

    y = gridtop + 14
    section(y + 4, "PROGRAM (FIXED)")
    y += 14
    rows = [
        ("SIT2 and Mock-2", lambda yy: bar(yy, D(2026, 10, 5), D(2026, 10, 23), "In flight, end date assumed", CARD, CH, hatch=True)),
        ("UAT (4 weeks)", lambda yy: bar(yy, D(2026, 10, 26), D(2026, 11, 20), "UAT  Oct 26 to Nov 20", ST)),
        ("Cutover", lambda yy: bar(yy, D(2026, 11, 23), D(2026, 12, 14), "Cutover and dress rehearsal", MA)),
        ("Go-live", lambda yy: (milestone(yy, D(2026, 12, 15), "Tech go-live Dec 15"), milestone(yy, D(2027, 1, 1), "Business go-live Jan 1", OR))),
        ("Hypercare", lambda yy: bar(yy, D(2027, 1, 1), D(2027, 2, 12), "Hypercare and first month-end close", ST)),
    ]
    for lab, fn in rows:
        label(y, lab)
        fn(y)
        y += 40
    y += 10
    b.append(f'<line x1="20" y1="{y}" x2="{dx(end)}" y2="{y}" stroke="{MUTED}" stroke-width="0.75"/>')
    y += 22
    section(y, "PERFORMANCE ASSURANCE WORKSTREAM")
    y += 14
    prow = [
        ("0  Mobilize", D(2026, 10, 5), D(2026, 10, 16), "Charter, team, ECS, stubs", BL),
        ("1  Shift-left baselines", D(2026, 10, 5), D(2026, 10, 30), "Measure in SIT2 now, fix code early", BL),
        ("2  Design and build", D(2026, 10, 7), D(2026, 11, 6), "Tier-1 set, workload, scripts, data", CH),
        ("3  Execute in pre-prod", D(2026, 11, 2), D(2026, 11, 20), "Cycles 1 to 4", OR),
        ("4  Tune and retest", D(2026, 11, 16), D(2026, 12, 3), "Fix, re-run, report", MA),
        ("5  PRD readiness", D(2026, 12, 7), D(2026, 12, 23), "Parity checks, safe PRD smoke", ST),
        ("6  Hypercare watch", D(2027, 1, 1), D(2027, 2, 12), "Same KPIs as live alerts", ST),
    ]
    for lab, s, e, txt, c in prow:
        label(y, lab)
        bar(y, s, e, txt, c, CH if c == OR else "#FFFFFF")
        y += 40
    milestone(y, D(2026, 10, 9), "Steering approval Oct 9", OR)
    milestone(y, D(2026, 12, 4), "Performance go / no-go Dec 4", OR, right=False)
    label(y, "Gates")
    y += 40
    # protected window callout
    b.append(text(dx(D(2026, 11, 2)) + 6, gridtop + 18, "Protected pre-prod window Nov 2 to Dec 4", 12.5, OR, "bold"))
    # thanksgiving
    tx = dx(D(2026, 11, 26))
    b.append(f'<line x1="{tx}" y1="{gridtop}" x2="{tx}" y2="{gridbot}" stroke="{MA}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    b.append(text(tx + 4, gridbot + 18, "Thanksgiving Nov 26", 12, MA))
    return 1730, 720, b


# ------------------------------------------------------------------ 3. Pyramid
def pyramid():
    b = []
    cx = 560
    tiers = [
        (40, 210, 160, "TIER 1", "~35 E2E scenarios", ["NeoLoad: load, stress, endurance", "Concurrent mix at design peak"], OR, CH),
        (220, 390, 360, "TIER 2", "~60 to 80 component checks", ["Top interfaces and batch jobs", "Volume injection, no UI scripting"], CH, "#FFFFFF"),
        (400, 570, 540, "TIER 3", "Everything else (hundreds of objects)", ["Telemetry watch during SIT2 and UAT", "Promote any outlier to Tier 2"], ST, "#FFFFFF"),
    ]
    prev = 0
    for ytop, ybot, half, lab, head, rows, fill, tc in tiers:
        tophalf = prev
        pts = f"{cx - tophalf},{ytop} {cx + tophalf},{ytop} {cx + half / 1},{ybot} {cx - half},{ybot}"
        if tophalf == 0:
            pts = f"{cx},{ytop} {cx + half},{ybot} {cx - half},{ybot}"
        b.append(f'<polygon points="{pts}" fill="{fill}" stroke="#FFFFFF" stroke-width="4"/>')
        prev = half
        my = ybot - 62 if lab == "TIER 1" else ytop + 48
        b.append(text(cx, my, lab, 15, tc, "bold", "middle"))
        b.append(text(cx, my + 24, head, 16 if lab != "TIER 1" else 14.5, tc, "bold", "middle"))
        if lab != "TIER 1":
            b.append(lines(cx, my + 50, rows, 13.5, tc, "normal", "middle"))
    # Tier1 descriptions outside left
    b.append(lines(40, 120, ["Scripted end-to-end with", "NeoLoad: load, stress and", "endurance at design peak"], 13.5, BODY))
    b.append(line(205, 135, 432, 168, CH, 1.2))
    # Right panel: scoring
    x = 1130
    b.append(rect(x, 40, 450, 530, NOTE, 12, NOTEB, 1))
    b.append(text(x + 24, 78, "HOW AN OBJECT EARNS ITS TIER", 15, CH, "bold"))
    b.append(text(x + 24, 112, "Risk score = Volume x Criticality x Complexity", 14, CH, "bold"))
    b.append(text(x + 24, 134, "each scored 1 to 5, so 1 to 125", 13, BODY))
    rules = [("48 and above", "Tier 1", OR, CH), ("20 to 47", "Tier 2", CH, "#FFFFFF"), ("below 20", "Tier 3", ST, "#FFFFFF")]
    for i, (r, t, f, tc) in enumerate(rules):
        y = 160 + i * 52
        b.append(rect(x + 24, y, 110, 38, f, 6))
        b.append(text(x + 79, y + 25, t, 14, tc, "bold", "middle"))
        b.append(text(x + 150, y + 25, r, 14, CH))
    b.append(text(x + 24, 340, "Automatic Tier 1 overrides", 14, CH, "bold"))
    b.append(lines(x + 24, 366, ["Regulatory: DRC Mexico CFDI, tax", "Financial truth: CFIN JE feed, trial balance",
                                 "Known pain: VIM", "Revenue: truck order to invoice",
                                 "Shared choke points: OneSource, number", "ranges, Cloud Connector, JMS"], 13.5, BODY, lh=24))
    # Left arrow: promotion
    b.append(text(x + 24, 530, "Any Tier 3 outlier seen in telemetry is promoted.", 13.5, OR, "bold"))
    return 1600, 590, b


# ------------------------------------------------------------------ 4. Scaling
def scaling():
    b = []
    cols = [
        ("A", "RESPONSE TIME AND SINGLE-THREAD RUNTIME", "Does not scale with capacity", BL,
         ["Same CPU generation and same data", "volume means about the same result", "in pre-prod and PRD."],
         ["VSM truck configuration step", "Single batch job runtime", "One OneSource call, one CFDI stamp"],
         "Test at real single-user and peak pacing. Pre-prod result is the PRD forecast."),
        ("B", "THROUGHPUT AND CONCURRENCY", "Scales with SAP capacity, not linearly", CH,
         ["Pre-prod is about 50% of PRD, so", "50% of design load in pre-prod is", "roughly 100% PRD-equivalent."],
         ["Concurrent Fiori and GUI users", "Billing run invoices per hour", "CFIN JE lines posted per hour"],
         "Step to 50% then push to the break point. PRD = measured x ratio x 0.85 derate."),
        ("C", "FIXED SHARED AND EXTERNAL LIMITS", "Same limit in pre-prod and PRD", OR,
         ["Bottlenecks outside the SAP", "app and HANA tiers do not get", "bigger in production."],
         ["BTP tenant, JMS, EOIO queues", "Cloud Connector, number range locks", "OneSource, PAC, Pega, legacy"],
         "Test at full 100% to 150% PRD design load. Half load here hides the real failure."),
    ]
    for i, (k, h, s, c, why, ex, rule) in enumerate(cols):
        x = 20 + i * 527
        tc = CH if c == OR else "#FFFFFF"
        b.append(rect(x, 20, 507, 96, c, 10))
        b.append(f'<circle cx="{x + 34}" cy="68" r="18" fill="{"#FFFFFF" if c != OR else CH}"/>')
        b.append(f'<text x="{x + 34}" y="{74}" font-family="{FONT}" font-size="18" font-weight="bold" fill="{c if c != OR else "#FFFFFF"}" text-anchor="middle">{k}</text>')
        b.append(text(x + 66, 58, h, 15, tc, "bold"))
        b.append(text(x + 66, 84, s, 14, tc))
        b.append(rect(x, 126, 507, 300, CARD, 10))
        b.append(text(x + 20, 158, "Why", 13, MUTED, "bold"))
        b.append(lines(x + 20, 182, why, 14, BODY))
        b.append(text(x + 20, 262, "Examples", 13, MUTED, "bold"))
        for j, e in enumerate(ex):
            b.append(f'<circle cx="{x + 26}" cy="{281 + j * 24}" r="3.5" fill="{c}"/>')
            b.append(text(x + 38, 286 + j * 24, e, 14, BODY))
        b.append(rect(x + 14, 358, 479, 56, "#FFFFFF", 8, NOTEB, 1))
        # wrap rule into 2 lines
        words, l1, l2 = rule.split(), "", ""
        for wd in words:
            if len(l1) + len(wd) < 58 and not l2:
                l1 += (" " if l1 else "") + wd
            else:
                l2 += (" " if l2 else "") + wd
        b.append(lines(x + 28, 381, [l1, l2], 13, CH, "bold", lh=20))
    # Load ladder
    y0 = 460
    b.append(text(20, y0, "PRE-PROD LOAD LADDER (percent of PRD design peak; design peak = 1.5 x measured peak hour)", 15, CH, "bold"))
    steps = [("Calibrate", "Single user and 10%", "Confirm scaling ratio", BL),
             ("Step 1", "50% design load", "About 100% PRD-equivalent for class B", CH),
             ("Step 2", "100% design load", "Class C limits at full PRD volume", MA),
             ("Step 3", "Ramp to break", "Find the knee, headroom margin", OR),
             ("Soak", "50% for 8 hours", "Memory growth, queue drift", ST)]
    for i, (h, l1, l2, c) in enumerate(steps):
        x = 20 + i * 316
        hgt = [40, 70, 100, 130, 70][i]
        base = y0 + 200
        b.append(rect(x, base - hgt, 296, hgt, c, 6))
        b.append(text(x + 14, base - hgt + 26, h, 15, CH if c == OR else "#FFFFFF", "bold"))
        b.append(text(x, base + 26, l1, 14, CH, "bold"))
        b.append(text(x, base + 46, l2, 13, BODY))
    return 1600, 720, b


GRAPHICS = [
    ("01-test-architecture", architecture, "Performance test architecture: where load enters and where we measure",
     "S/4HANA pre-prod on RISE, BTP Integration Suite, DataStage and CFIN, and the legacy and SaaS endpoints"),
    ("02-timeline", timeline, "Ten weeks to tech go-live: the performance workstream against the program",
     "Execution runs in parallel to UAT in a protected pre-prod window, with a performance gate on Dec 4"),
    ("03-risk-tier-pyramid", pyramid, "Risk-tiered scope: test deeply where the risk is",
     "Replace several hundred bespoke tests with about 35 scripted scenarios, about 70 component checks, and telemetry"),
    ("04-scaling-model", scaling, "Reading results from a 50% pre-prod",
     "Three classes of metrics, three different rules for translating to production"),
]

for name, fn, title, sub in GRAPHICS:
    w, h, body = fn()
    content = "".join(body)
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(svg(w, h, content, title, sub))
    with open(os.path.join(OUT, f"{name}-deck.svg"), "w") as f:
        f.write(svg(w, h, content, title, None, deck=True))
print("ok")
