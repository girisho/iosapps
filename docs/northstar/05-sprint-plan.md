# 5 · End‑to‑End Build Plan & Sprints

Two‑week sprints. The phase ordering mirrors the deck's roadmap — **Protect first, then grow** — because each phase ships measurable value and creates the baseline the next phase needs.

## 5.1 Phases (map to the deck roadmap)

| Phase | Deck step | Goal | Headline metric |
|-------|-----------|------|-----------------|
| **P0 Foundations** | — | Ingestion, lakehouse, config schema, engine skeleton, agent runtime | Pipeline green on reference extract |
| **P1 Protect margin** | Step 1 | Incentive coverage & determination at order entry, observe mode | credit‑memo rate, margin leakage $ |
| **P2 Free the cash** | Step 2 | Cluster reinvoice/DSR by root cause; fix biggest causes | reinvoice rate, DSO |
| **P3 De‑risk & track** | Step 3 | Invoicing & component study + Mexico CFDI; begin consistency tracking | CFDI events, rules banked |
| **P4 Grow the business** | Step 4 | Incentive effectiveness, give‑away analysis, program ROI, governance | incremental volume, ROI |
| **P5 Productize & scale** | — | Multi‑tenant onboarding, deploy‑time agents, self‑serve config | time‑to‑first‑report ↓ |

Roughly one quarter per phase for a small team; P0 ~6–8 weeks. Adjust to team size.

## 5.2 P0 — Foundations (Sprints 0–4)

**Sprint 0 — Discovery & scaffolding**
- Secure a reference SAP extract (orders, items, condition records, VBRK/VBRP, change docs, memos).
- Stand up repo, CI/CD, IaC skeleton, lakehouse + Postgres, secrets manager.
- Draft the **configuration schema** (condition‑type→component, table→entity, segment defs, lifecycle steps). *DoD: schema validates the reference config.*

**Sprint 1 — Ingestion**
- SAP extraction (CDS/OData + RFC) into bronze; CDC transport for order/billing events.
- dbt bronze→silver: build the **transaction‑lifecycle spine**, segmented dealer/fleet.
- *DoD: reference extract lands and conforms; row‑count & integrity tests pass.*

**Sprint 2 — Engine v0 (one component, one segment)**
- Implement Expected‑vs‑Actual for **incentive coverage**, dealer segment: peer/consistency baseline + amount bands; store Δ with provenance and $ value.
- *DoD: engine flags a known missing‑SPA case on the reference data with the right $ gap.*

**Sprint 3 — Agent runtime + first tools**
- Stand up Managed Agents; create the agent‑config + version pipeline (`agents.create` once, reference by ID).
- Build core custom tools: `query_warehouse`, `get_expected`/`get_actual`, `open_case`. Credentials host‑side.
- *DoD: a Determination Agent investigates a flagged delta and opens a case end‑to‑end.*

**Sprint 4 — Case store, UI shell, observe mode**
- Postgres case/workflow store + audit log; React app shell with a case‑review screen; alerting plumbing.
- *DoD: a human can review, accept/dismiss a case; every action is audited.*

## 5.3 P1 — Protect margin (Sprints 5–9)

- Complete **determination + eligibility** coverage (SPA/eDeal OTC_I107, VPAS OTC_I008; Stock→Sold re‑determination; date windows, program limits).
- Determination & Eligibility Agents at near‑real‑time on new/changed orders, **observe mode**.
- Margin rollup v1 + the "how much discount are we giving away?" view per dealer/program/segment (the margin bridge).
- Baseline‑confidence scoring so analysts know how much to trust each flag.
- *Phase DoD: on reference data, the system reproduces real determination errors with $ impact; champion validates a sample; leakage baseline established.*

## 5.4 P2 — Free the cash (Sprints 10–14)

- **Reinvoicing Root‑Cause Agent:** cluster Z601/Z701/DSR/manual‑journal population; identify repeat‑offender dealers & materials; learn entry signatures that predict a future correction.
- Order‑Change Agent: churn/gaming/unposted‑penalty detection (Step 28, OTC_I023, G‑1873H).
- Feedback loop: corrections feed the determination model (the loop starts compounding).
- *Phase DoD: top reinvoice root causes quantified; predicted‑correction precision/recall meets target; reinvoice‑rate baseline + projected DSO impact.*

## 5.5 P3 — De‑risk & track (Sprints 15–19)

- **Invoicing Agent:** per‑segment invoice characterization; fleet ZSPV/ZDIF Cust‑Exp‑Price drift; duplicate VIN; account‑key checks. Surcharge & freight component studies.
- **Compliance Agent (MX/LATAM):** CFDI/SAT UUID linkage checks, reissue‑rate as audit exposure, export Z201 / intercompany.
- **Governance Agent v1:** discover → score → ratify workflow; begin banking rules; drift watch.
- *Phase DoD: invoicing deviations surfaced with $; CFDI exposure flagged; first governance rules ratified & monitored.*

## 5.6 P4 — Grow (Sprints 20–24)

- **Incentive‑Effectiveness Agent:** pair incentive exposure with volume response; whitespace finder; waste finder; pre‑launch **program ROI** model.
- Govern‑from‑consistency at scale: rule set grows from the uncontested end inward.
- Executive "maturity curve" reporting (React→Catch→Prevent→Shape).
- *Phase DoD: a program‑ROI prediction validated against a real past program; give‑away reduction quantified.*

## 5.7 P5 — Productize & scale (ongoing)

- **Deploy‑time agents:** Mapping Agent, Behavior‑Study Agent, Data‑Quality Agent (the repeatable sales/onboarding motion).
- Self‑serve configuration tooling + config validation; tenant provisioning automation (Terraform).
- Edition packaging (Protect / Protect+Comply / Grow); usage metering for value‑share pricing.
- *Phase DoD: a new customer goes extract → priced report in days, not months.*

## 5.8 Cross‑cutting workstreams (every sprint)

- **Security & compliance:** least‑privilege SAP access, tenant isolation, audit log, data residency, secrets hygiene (no creds in prompts), pen‑test before first customer go‑live.
- **Eval harness for agents:** a labeled set of known deltas/corrections to measure agent precision/recall and catch regressions when prompts/models change. Treat agent prompts like code — versioned, reviewed, eval‑gated.
- **Cost governance:** Haiku‑first triage, prompt caching of the stable config prefix, batch the non‑interactive runs, per‑tenant token telemetry.
- **Observe → Alert → Prevent graduation:** every flag type starts in observe mode; promote only after precision clears a bar with the customer.

## 5.9 Team shape (lean)

Data engineer (ingestion/lakehouse) · ML/analytics engineer (the engine) · 1–2 backend engineers (orchestrator, tools, API) · agent/prompt engineer (agent library + evals) · frontend engineer · SAP‑pricing SME (part‑time, validates mappings & findings) · product/GTM. Scale by adding engine + agent coverage breadth.
