# Project NorthStar - SAP S/4HANA 2023 FPS02 to SPS06 upgrade
## Handoff notes (as of Sun 18 Oct 2026)

CONFIDENTIAL AND PROPRIETARY TO INTERNATIONAL

Use this file to continue in a new Claude chat: attach it plus the files you need, and say "Continue the NorthStar SPS06 upgrade work from these handoff notes."
Every date and status below comes from the plan data behind `NorthStar_SPS06_Upgrade_Plan.xlsx` (plan v4.0 (18 Oct 2026)).

---

## 1. What the project is

- **Customer / programme:** International Motors (INTL), Project NorthStar (SAP S/4HANA on RISE with SAP, Private Cloud Edition). Go-live 1 Jan 2027.
- **Upgrade:** SAP S/4HANA 2023 **FPS02 to SPS06** (S4CORE 108 SP06; SAP_BASIS and SAP_UI 758 SP06). This is an update within one release. SAP numbers the stacks FPS00-FPS02 (feature packs), then SPS03 onwards (support packs only); the Upgrade Guide's own example is "2022 FPS02 to SPS03".
- **Scope:** US, Canada, Mexico; English only; SAP Build Work Zone Standard; CFIN runs in the same S/4.
- **Path:** Sandbox XS4, then Dev DS4, QA QS4, Pre-prod SS4, Prod PS4. N+1 copies DS5 and QS5 (SAP "temporary landscape").
- **SAP ECS runs SUM** through service requests; INTL Basis owns the SRs.
- **Release 2 is paused**; no test automation (all regression manual).

### Roles (allocation you set)

| Team | Who | Scope |
|---|---|---|
| INTL Basis | Girish Ogirala (lead) + 1 onsite + 2 offshore | Technical owner of the upgrade; SRs, copies, post-processing, transports, weekend coordination |
| INTL Security | Security team (collaborates with Basis) | SU25/SU24, PFCG roles, GRC AC post-steps, SailPoint and SDMI users |
| INTL PMO | Project NorthStar PMO | Plan, gates, steering, communications |
| INTL Testing | NorthStar test management | Regression scope, qTest/ADO tracking, UAT coordination |
| Business (UAT) | Business product owners and IT leads | UAT execution and business sign-off |
| PwC Tech | PwC technical team | SPDD/SPAU, notes, custom code, ATC, Fiori custom apps, RICEFW unit tests |
| PwC Functional | PwC functional streams | SI-check application items, regression testing, integration flows |
| PwC Data Migration | PwC data migration (Syniti) | Mock loads, Syniti alignment, migration validation on SPS06 |
| SAP ECS | SAP Enterprise Cloud Services (via SRs) | System copies, SUM execution, HANA/kernel, backups, technical FES upgrade |
| SAP MaxAttention | SAP MaxAttention engagement team | Plan safeguarding, issue escalation, weekend/go-live support |
| SAP BTP | SAP BTP team (from SAP) | AFC, MBC, DRC, Work Zone tenants, Cloud Connector guidance |
| Vendors | OpenText, Thomson Reuters, SailPoint, Syniti | Compatibility statements and partner-specific steps |

PwC: functional and technical (STP/Ariba, OTC, RTR, ITD, CFIN, OpenText VIM, AFC, DRC, MBC, OneSource, GTS). You (Girish Ogirala, INTL Basis lead, 1 onsite + 2 offshore) own Basis, collaborate with SAP Security, and manage SAP MaxAttention, ECS, BTP and incidents.

### Systems

| SID | Role | Clients | Copy | Upgrade window | Note |
|---|---|---|---|---|---|
| XS4 | Sandbox (rehearsal) | tbc | Copy of DS4, 21-22 Oct | Sat 24 Oct | Prep on track since 15 Oct; copy SR raised; SR 31018471 reused for the SUM rerun |
| DS4 | Development | 110 | - | Sat 31 Oct | Dev lock from Fri 30 Oct (SUM uptime) |
| DS5 | Temporary Dev / N+1 Dev | tbc | Copy of DS4, 27-28 Oct | Tue 1 Dec | Fallback until G4 |
| QS4 | QA (SIT) | 100, 200 | - | Sat 7 Nov | SIT2 in client 200 until 6 Nov |
| QS5 | Temporary QA / N+1 QA | tbc | Copy of QS4, 4-5 Nov | Thu 3 Dec | Fallback until G4 |
| SS4 | Pre-production (UAT) | 100 | - | Fri-Sat 13-14 Nov | Mock3 + performance test to 6 Nov; UAT from 9 Nov |
| PS4 | Production | tbc | - | Fri-Sat 20-21 Nov | Cutover 7-31 Dec; go-live 1 Jan 2027 |
| QL4 | SLT server for Central Finance | - | - | Suspend/resume around QS4 and SS4 | Confirm DMIS compatibility |
| QL5 | SLT server for Central Finance | - | - | Repoint to QS5 after copy |  |
| DG4 | SAP GTS Development | tbc | - | Paused during DS4 window | GTS release to confirm |
| QG4 | SAP GTS QA (client 300 = UAT) | 300 (UAT) + SIT client tbc | - | Paused during QS4 and SS4 windows | No GTS pre-production exists |
| BTP | AFC, MBC, DRC (MX), Work Zone Standard | - | - | Connection checks after each window | Copies stay disconnected |

---

## 2. History of this engagement (3-18 Oct 2026)

**Fri 3 Oct - strategy, plan v1, side-effect register, deck**
- You asked for a realistic upgrade strategy and plan embedded in the project plan, around SIT1/SIT2 and Mock Load 2; INTL roles Basis/Security/PMO, PwC functional; sandbox basic validation, DS4 no interference, QS4-200 full testing, SS4 second round during UAT, then PS4. Inputs: Testing Overview (5 Mar 2026), Maintenance Planner software catalog (SWC), then the side-effect report (SER).
- Your answers: dates shifted (SIT1 extended one week, running in parallel with SIT2; SIT2 started Mon 28 Sep as planned); N+1 exists, active first week of November, no transports moved yet; Sandbox in scope; ECS executes SUM; CFIN in the same S/4; deliverables Excel + NorthStar PPTX.
- Delivered: `SAP_Notes_Side_Effect_Register_SPS06.xlsx` (135 in-scope notes incl. 2 HotNews 3777415 and 3563542; 178 conditional) - committed that day; strategy deck and plan v1.
- You asked to **stop pushing to git until you ask** (in force throughout; you lifted it once on 18 Oct with "push").
- You asked for a Tricentis automation variant incl. QS4-200 to QS5-100 transports: delivered as the `*_Option_Automation` files.

**Tue 6 Oct - Plan on a Page update (v2)**
- You shared the updated Plan on a Page (image in folder 03) and decided **no automation** as the main plan, keeping the automation version as an alternative.
- Your answers: DRC = SAP Document and Reporting Compliance deployment for Mexico; "TR Onsite" = Thomson Reuters on site for OneSource indirect tax; Go/No-Go at UAT end, the rest TBC. (QS4 inside SIT2 on 24-25 Oct was chosen then; superseded on 17 Oct.)

**Sat 17 Oct (morning) - blog research**
- Top posts found (popularity could not be measured; SAP sites blocked by this environment): SUM stack-update steps (member blog), "S/4HANA 2023 FPS00 Upgrade" (member), "RISE upgrade - information and tips" (SAP). Recommendation: use SAP's Upgrade Guide for Private Edition 2023 (UPGR_PE2023) for steps, the RISE tips blog for working with ECS. Extra tip: time the XPRAS_AIMMRG phase in Sandbox (KBA 2928403). Full answer is in the transcript (folder 05).

**Sat 17 Oct - 20-item update, plan v3** (inputs: SR 31018471 PDF, MP attachments zip, UPGR_PE2023.pdf)
- SR 31018471 (BASIC_1.5.09, XS4; window 9 Oct 02:45-10:45 UTC) paused at Configuration 12% on the SI-check: the minimum version of Note 2502552 was missing; on 12 Oct 2502662 was entered by mistake; SNOTE is blocked while SUM runs (TN687); ECS reset SUM on 14 Oct.
- Maintenance Plan 1002693650 (XS4 only, SUM 2.0 SP26): Fiori for S/4HANA 2023 02 to 03 FPS; FES 2023 stays 02; GRC AC 12.0 SP29 to SP32; VIM FND/INV SP03 to SP04, O2C/P2P SP01 to SP02; Ariba CI 21 to 27; HANA 2.00.089.5 (SPS08) and kernel 916 in the download list.
- Your answers: QL4/QL5 are SLT servers for Central Finance (not upgraded); copy DS4 to XS4 then rerun SUM; QS4 straight after SIT2 with **weekend windows** (DS4 too) to minimise SIT2 defect work; DS5/QS5 are the fallback until G4, then upgraded; Release 2 paused.
- Delivered v3: planner workbook, HTML dashboard, BPMN end-to-end and per-system diagrams, landscape and sequence diagrams, vendor questions with e-mail drafts (OpenText, Thomson Reuters, SailPoint, Syniti), Sandbox test plan (30 tests), Guide checklist, RAID, RACI.
- Recommendation given: **yes, e-mail OpenText** (VIM support packs move in the stack and the SER lists no OpenText components); drafts are in the Vendor Questions tab.

**Sun 18 Oct - plan v4 and dashboard redesign**
- You asked for an uncluttered executive dashboard, a positive, on-track status from Thu 15 Oct (the approach change), and a simple MS Project-style plan.
- Your answers: keep Sandbox dates; done = copy SR raised with ECS, Notes in DS4, Maintenance Planner per system; Excel only with detail behind; one neutral history line on the dashboard.
- Delivered v4 (current): Schedule sheet first (verb + team, MS Project style, Gantt), Exec Summary feeding the dashboard, new one-screen dashboard with drill-down.
- You asked whether the Upgrade Guide's notes were included: 43 of 51 were spread across tabs. Delivered `NorthStar_SPS06_Upgrade_Guide_Notes.xlsx` with all 51.
- Everything was pushed to GitHub `girisho/iosapps`, branch `claude_go/gifted-johnson-r3uvto` (commit 7fc97c1).

---

## 3. Current plan (v4) - where things stand on 18 Oct

**Overall: On Track.** Sandbox preparation is completing on plan.

Status of started items:
- 0.1 Triage SAP side-effect notes (PwC Tech): **Complete**
- 0.2 Plan XS4 stack and request update (INTL Basis): **Complete**
- 0.3 Close first XS4 update run (SUM reset) (SAP ECS): **Complete**
- 0.4 Approach set: Sandbox = copy of DS4 (INTL Basis): **Complete**
- 1.1 Align plan with PwC Tech (PwC Tech): **Complete**
- 1.2 Review plan (functional streams) (PwC Functional): **On Track**
- 1.3 Implement SAP Notes in DS4 (INTL Basis): **Complete**
- 1.4 Request DS4 to XS4 copy from ECS (INTL Basis): **Complete**
- 1.5 Create Maintenance Planner plans (INTL Basis): **Complete**
- 1.6 Run SI-check and pre-checks (INTL Basis): **On Track**

Phases:

| ID | Phase | Dates | Status |
|---|---|---|---|
| 0 | Start-up | 02 Oct - 15 Oct | Complete |
| 1 | Prepare Sandbox | 15 Oct - 28 Oct | On Track |
| 2 | Sandbox XS4 | 21 Oct - 29 Oct | Not Started |
| 3 | Development DS4 (+ DS5 copy) | 27 Oct - 13 Nov | Not Started |
| 4 | QA QS4 (+ QS5 copy) | 04 Nov - 12 Nov | Not Started |
| 5 | Pre-production SS4 | 09 Nov - 04 Dec | Not Started |
| 6 | Production PS4 | 14 Nov - 25 Nov | Not Started |
| 7 | N+1 DS5 / QS5 | 01 Dec - 04 Dec | Not Started |
| 8 | Close-out | 23 Nov - 01 Jan | Not Started |

Milestones and gates:

| ID | Date | Milestone | Type | Criteria / notes |
|---|---|---|---|---|
| G0 | Thu 22 Oct 2026 | Ready for Sandbox | Gate | Notes 2399707/2502552 in DS4 and transported; SI-check RC < 8 in DS4 and QS4; SRs accepted with windows; MPID per system; copy isolation checklist signed |
| XS4 | Sat 24 Oct 2026 | Sandbox XS4 on SPS06 | Upgrade | Downtime Sat 24 Oct, Sun 25 contingency |
| G1 | Thu 29 Oct 2026 | Sandbox sign-off | Gate | XS4 upgrade clean; Sandbox Test Plan "Yes" items passed; SPDD/SPAU and note effort sized; downtime measured; vendor answers received or tracked |
| DS4 | Sat 31 Oct 2026 | Development DS4 on SPS06 | Upgrade | Downtime Sat 31 Oct, Sun 1 Nov contingency; DS5 live as temporary Dev |
| G2 | Wed 04 Nov 2026 | Dev ready | Gate | SPDD/SPAU, note and role transports released; no blocking unit-test failure; zero priority-1 ATC findings |
| SIT2 | Fri 06 Nov 2026 | SIT2 ends (QS4-200) | Project | Plan on a Page |
| QS4 | Sat 07 Nov 2026 | QA QS4 on SPS06 | Upgrade | Downtime Sat 7 Nov, Sun 8 contingency |
| G3 | Thu 12 Nov 2026 | Go for pre-production | Gate | P1 re-run >= 95% pass; zero open Sev1/Sev2 upgrade defects; CFIN, GTS, BTP integrations green; security passed; migration objects load on SPS06 |
| SS4 | Sat 14 Nov 2026 | Pre-production SS4 on SPS06 | Upgrade | Downtime Fri night 13 - Sat 14 Nov, Sun 15 contingency |
| G4 | Thu 19 Nov 2026 | Go for production | Gate | SS4 stable; UAT running on SPS06 without upgrade blockers; performance delta acceptable; legacy end-to-end OK |
| PS4 | Sat 21 Nov 2026 | Production PS4 on SPS06 | Upgrade | Downtime Fri night 20 - Sat 21 Nov, Sun 22 contingency |
| G5 | Wed 25 Nov 2026 | Upgrade closed | Gate | PS4 technical verification signed; UAT clean on SPS06; open items handed to Go/No-Go |
| GNG | Mon 30 Nov 2026 | Go / No-Go (30 Nov - 4 Dec) | Project | Plan on a Page (at UAT end) |
| N+1 | Thu 03 Dec 2026 | DS5 / QS5 on SPS06 | Upgrade | DS5 Tue 1 Dec, QS5 Thu 3 Dec |
| CUT | Mon 07 Dec 2026 | Cutover starts (7 - 31 Dec) | Project | Plan on a Page |
| GL | Fri 01 Jan 2027 | Go-live | Project | Plan on a Page |

Transport windows A-E and the DS5/DS4 dual-maintenance rule (30 Oct - 13 Nov) are in the Transport Windows tab.

Plan B (ECS cannot meet a window, or G1 fails): shift the chain by one week - XS4 31 Oct, DS4 7 Nov (after SIT2, so DS5 is not needed for SIT2 fixes), QS4 14 Nov, SS4 21 Nov, PS4 28 Nov (Thanksgiving weekend). G5 moves to Wed 2 Dec, inside the Go/No-Go week; UAT weeks 1-2 run on FPS02 and weeks 3-4 on SPS06.

Plan C (G3 fails): SS4 and PS4 stay on FPS02 and go live on FPS02. DS5 and QS5 (FPS02 copies) become the delivery line for fixes to SS4 and PS4; DS4 and QS4 stay on SPS06 as the post-go-live upgrade line. Remaining systems are upgraded after hypercare.

---

## 4. Decisions

- **D1** Copy DS4 to XS4, then rerun SUM on XS4; Sandbox preparation from Thu 15 Oct (USER)
- **D2** Copy DS4 > DS5 and QS4 > QS5, then upgrade DS4 and QS4 (SAP temporary landscape, UG 3.1) (USER)
- **D3** Weekend windows: DS4 31 Oct, QS4 7 Nov, SS4 13-14 Nov, PS4 20-21 Nov (USER option 1 + weekend)
- **D4** DS5/QS5 stay FPS02 as fallback until G4, then upgrade w/c 30 Nov (USER)
- **D5** No test automation (USER)

Open decisions:
- **D-O1** SDMI in uptime (default, recommended) or forced in downtime (must be stated in the SR, UG 6.1) (recommendation: Recommend default uptime; owner INTL Basis; by Thu 22 Oct 2026)
- **D-O2** connect XS4 to DG4 for GTS tests? Recommend no; prove GTS in QS4 + QG4 (recommendation: Recommend no; owner PwC Functional (GTS); by Thu 22 Oct 2026)
- **D-O3** use Data Transition Validation (Note 3117879) for QS4-200 finance reports? Optional (recommendation: Optional; owner INTL Test Lead; by Fri 23 Oct 2026)
- **D-O4** Fiori follow-ups by INTL Basis or ECS CAS (BASIC_1.5.03, billable) (recommendation: Recommend INTL Basis; owner INTL Basis; by Thu 22 Oct 2026)
- **D-O5** SPDD/SPAU by PwC Technical or ECS billable package (TO_NWABAP_1.5.08) (recommendation: Recommend PwC unless XS4 shows high volume; owner INTL Basis; by Wed 28 Oct 2026)

## 5. High risks (each has an owner and a response)

- **R1** (High) ECS cannot schedule three copies and six SUM runs on the requested dates. Response: Copy SR for XS4 raised; remaining SRs Mon 19 Oct; MaxAttention escalation; Plan B (+1 week)
- **R2** (High) SAP updates Note 2502552 between systems and the SI-check pauses SUM. Response: Check the note version 48 h before each window; re-run SI-check
- **R3** (High) Copies (XS4, DS5, QS5) send data to GTS, SLT, MBC/banks, DRC/PAC, Ariba, OneSource, SailPoint. Response: Isolation checklist (0.10) executed and evidenced before any user logs on
- **R4** (High) Five consecutive weekend windows (24 Oct - 22 Nov) for a 3-person Basis team. Response: Rota across onsite/offshore; ECS + MaxAttention cover; no Basis change work on weekdays after a window
- **R6** (High) QS4 regression window is 4 days (9-12 Nov). Response: P1 scripts only; FPS02 baseline; TR onsite the same week; Sandbox evidence first
- **R9** (High) Partner confirmations (OpenText, SailPoint, Syniti, TR) not received before G1 / G3. Response: E-mails sent 19-20 Oct; answers due 28 Oct; hold at G3 if open

## 6. Assumptions

- **A1** Project dates per Plan on a Page (9/21) and user updates: SIT2 28 Sep - 6 Nov (QS4-200); Mock3 19 Oct - 6 Nov and performance test 14 Oct - 6 Nov (SS4-100); UAT 9 Nov - 4 Dec (SS4-100); Go/No-Go at UAT end; cutover 7 - 31 Dec; go-live 1 Jan 2027
- **A2** Downtime per system is about 8 h (XS4 SR window); actual duration is measured in XS4 (1.11)
- **A3** Copies are taken from backups, so DS4 and QS4 stay available during the copy (ECS to confirm)
- **A4** No test automation; all regression is manual (USER)
- **A5** Release 2 is paused (USER); N+1 activity is limited to fallback and fixes
- **A6** PS4 holds no business data before cutover (7 Dec)
- **A7** Times are US Central (SR log shows America/Chicago); ECS windows are agreed in UTC

---

## 7. Open items needing your input

**Assumptions I made in v4 (confirm or change in Exec Summary / Schedule):**
1. PwC Functional review finishes Mon 19 Oct; Steering approves the plan Tue 20 Oct.
2. Copy SR number for DS4 to XS4 is not known: shown as "raised (add no.)" in SR Tracker.
3. Leadership ask "Confirm weekend cover 24 Oct - 22 Nov" is my suggestion.

**Questions still open from 17 Oct:**
4. QG4 SIT client number and the GTS release.
5. Which source systems feed QL5 after it is repointed to QS5.
6. Client numbers for XS4, DS5, QS5 and PS4.
7. Is there a separate Java / Adobe Document Services instance? Is Advanced Variant Configuration used?
8. ECS service identifier and lead time for system copies.

**Upgrade Guide notes marked "Conditional - confirm" (7):** 178788 SAP GUI for HTML, 485741 changed translations of SAP objects, 2781530 Consolidation / Mass Processing, 2834255 S/4HANA Service WebClient UI, 2251604 and 3247591 separate Java instance, 2987015 Advanced Variant Configuration.

**Vendor questions to send Mon 19 Oct (answers due Wed 28 Oct):**
- OpenText: OT-1, OT-2, OT-3, OT-4, OT-5, OT-6, OT-7
- Thomson Reuters: TR-1, TR-2, TR-3, TR-4
- SailPoint: SP-1, SP-2, SP-3, SP-4, SP-5
- Syniti: SY-1, SY-2, SY-3, SY-4, SY-5, SY-6

**Possible additions (from the blog research, not yet in the plan):** Z package before the update; fast SPDD ticket turnaround with ECS; timing the XPRAS_AIMMRG phase in Sandbox.

**Not refreshed:** `NorthStar_SPS06_Upgrade_Strategy.pptx` reflects the 6 Oct plan (v2), not v4.

---

## 8. How to run the plan day to day

1. **Exec Summary tab:** set "As of", check overall status, headline, key messages, team alignment and asks.
2. **Schedule tab:** set Status per task and gate (drop-down). Phases, % complete, Milestones and Detail Plan follow automatically.
3. **Dashboard:** open `NorthStar_SPS06_Upgrade_Dashboard.html` in a browser, click "Update data", pick the saved workbook (or drop it on the page). It is read locally; nothing is uploaded. Do not rename sheets or column headers.

---

## 9. Your standing rules for this work

- No hallucinations: recheck before calling anything done; DO NOT FAKE information; cite sources (SR log, MP, Upgrade Guide section, SER, Plan on a Page, your statements).
- No test automation.
- Do not push to git unless you ask.
- Content is confidential and proprietary to International; keep deliverables as files.
- Clear roles, approximate durations and milestones; ask questions before planning.
- Style: International Motors / NorthStar brand (charcoal 272623, orange FF7144, maroon 5C1916, INTL blue 0062A2, steel 4E5659; Arial) for decks and Excel.

---

## 10. What is in this folder

| Folder | Contents |
|---|---|
| 01_Current_Deliverables | Plan workbook v4, executive dashboard (HTML), Upgrade Guide notes (51), side-effect notes register (135 in scope), diagrams (BPMN end-to-end, per-system cycle, landscape, sequence; SVG and PNG) |
| 02_Strategy_Decks_and_Options | Strategy deck (6 Oct, pre-v3), automation option deck and workbook (alternative only) |
| 03_Source_Inputs_You_Provided | Testing Overview, MP software catalog (SWC) and side-effect export (SER), SR 31018471 PDF, MP 1002693650 attachments, UPGR_PE2023.pdf, Plan on a Page image (6 Oct) |
| 04_Archive_Superseded | Plan v2 and v3 workbooks, v3 dashboard |
| 05_Conversation_History | Full text of our conversation (your messages and my replies) |

GitHub copy: `girisho/iosapps`, branch `claude_go/gifted-johnson-r3uvto`, folder `S4_SPS06_Upgrade/` (source inputs and transcript are only in this package).
