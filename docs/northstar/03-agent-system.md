# 3 · The Agent System

This is the part of NorthStar that turns a static analytics product into *Agentic* Pricing Intelligence — and it's the answer to "what agents do I run when I sell and deploy this?"

## 3.1 Two kinds of agents

1. **Deal/Deploy‑time agents** — you (the vendor) run these during the *sales motion and onboarding* of a new customer. They turn a raw SAP extract into a quantified leakage report and a working configuration, fast. This is what makes the "Behavior Study" engagement repeatable instead of a custom consulting project every time.
2. **Run‑time agents** — these run *continuously inside the customer's tenant* after go‑live, investigating deltas, clustering corrections, drafting governance rules, and producing the periodic intelligence.

Both are built on the **same agent runtime** and share a library of tools. The difference is only *when* they run and *who* triggers them.

## 3.2 Why agents (not just pipelines)

A deterministic pipeline can compute Δ. But the high‑value work — *investigating why a delta happened, deciding if it's a mistake vs. a rule, clustering hundreds of credit memos into a handful of root causes, drafting a defensible governance rule, writing the customer‑facing finding* — is open‑ended, multi‑step, and benefits from reasoning over heterogeneous evidence. That's exactly the "Should I build an agent?" sweet spot: complex, high‑value, recoverable (a human ratifies), and well within model capability.

Keep the division clean: **the engine computes deltas deterministically; the agents reason about them.** Don't ask an agent to do arithmetic the warehouse should do.

## 3.3 The agent library

Each agent is a persisted, versioned configuration (model + system prompt + tools) that you create once and reuse across every customer tenant.

### Deploy‑time agents (run during sell & onboard)

| Agent | Job | Triggered | Output |
|-------|-----|-----------|--------|
| **Mapping Agent** | Inspect a customer's SAP extract, propose the configuration mapping (condition types → components, tables → entities, segment definitions). Ask the human to confirm ambiguous mappings. | Onboarding, once per customer | A draft `config` (mappings, segments, lifecycle steps) for human ratification |
| **Behavior‑Study Agent** | Run the engine over the extract, then write the quantified leakage report: top leakage drivers, $ at stake, by segment/dealer/component. | Sales/POC, per extract | The deliverable that closes the deal — a priced findings report |
| **Data‑Quality Agent** | Profile the extract, flag gaps/coverage problems, estimate confidence in each component's expected. | Onboarding | A readiness scorecard ("what we can study today vs. what needs more data") |

### Run‑time agents (run continuously in the customer tenant)

| Agent | Job (maps to deck) | Cadence |
|-------|--------------------|---------|
| **Determination & Eligibility Agent** | For flagged orders (no expected SPA/VPAS, amount out of band, stale eligibility on Stock→Sold flips), investigate and assemble a case with evidence + $ gap | Near‑real‑time on new/changed orders, observe mode |
| **Invoicing Agent** | Characterize every invoice, surface deviations from segment normal (incl. fleet ZSPV/ZDIF Cust‑Exp‑Price drift, duplicate VIN, wrong account keys) | On billing events |
| **Reinvoicing Root‑Cause Agent** | Cluster the credit‑memo / DSR / debit‑memo / manual‑journal population by root cause; identify repeat‑offender dealers & materials; learn entry signatures that predict a correction | Daily/weekly batch |
| **Order‑Change Agent** | Study change behavior per dealer — frequency, lateness, cancel‑and‑rebook timed to date windows; flag systemic churners, gaming patterns, unposted penalties (G‑1873H) | Daily |
| **Compliance Agent (MX/LATAM)** | Flag broken CFDI/SAT UUID linkage, read reinvoice frequency as SAT exposure, extend Expected‑vs‑Actual to export Z201 / intercompany / declared value | On CFDI events |
| **Governance Agent** | Discover high‑consistency patterns → score (bank‑able vs. genuinely split) → draft a documented, auditable rule for human ratification → watch for drift | Weekly + on‑demand |
| **Incentive‑Effectiveness Agent (Grow)** | Pair incentive exposure with volume response; separate what drives sales from margin given away; find whitespace; model program ROI before launch | Monthly + pre‑program |

### Orchestration

A lightweight **Coordinator** agent (or a scheduler) fans work out to the specialist agents and consolidates their cases into the daily/weekly intelligence. Specialists run in their own isolated context with their own tools — they share the lakehouse and case store, not conversation history. Use parallel sub‑agents for fan‑out (e.g., one investigation per flagged order), kept asynchronous so the coordinator isn't blocked on the slowest one.

## 3.4 How the agents actually run (platform mechanics)

NorthStar's agents are built on **Claude Managed Agents** (`claude-opus-4-8` as the default reasoning model — see [`04-tech-stack.md`](04-tech-stack.md) for the model rationale). The mechanics that matter:

- **Create once, run many.** Each agent is a persisted, versioned object (`agents.create`). You store the agent ID and reference it from every session — you do **not** recreate the agent per run. Versioning lets you improve an agent's prompt/tools without breaking running customers, and pin a customer to a known‑good version.
- **Tools.** Agents get the built‑in toolset (bash, file ops, web fetch) **plus custom tools** that are the real integration surface:
  - `query_warehouse(sql)` — read gold/silver facts (deltas, cases, baselines).
  - `get_expected(component, keys)` / `get_actual(...)` — fetch a specific Expected/Actual pair with provenance.
  - `cluster_corrections(filter)` — run the correction‑clustering routine.
  - `propose_rule(pattern)` / `draft_finding(...)` — structured outputs for governance rules and report sections.
  - `open_case(...)` — write a case to the case store (the only "write" a run‑time agent does, and it's internal, not to SAP).
- **Custom tools keep secrets host‑side.** When an agent needs the SAP/warehouse credential, the call is executed by *your* orchestrator (which holds the credential) and the result is handed back to the agent — the agent's sandbox never sees the secret. For service integrations that speak MCP, use **vaults** so credentials are injected at egress and never enter a prompt.
- **Scheduled deployments.** The run‑time agents fire on a cron cadence (nightly reinvoice clustering, weekly governance discovery, monthly incentive effectiveness) — each firing is an autonomous session. No human has to kick them off.
- **Outcomes / rubric‑graded work.** For deliverables with a checkable definition of done (e.g., "the leakage report must have a $ figure per top‑10 driver, split by segment"), define the outcome as a rubric so the agent iterates until it passes.
- **Human‑in‑the‑loop gates.** Rule activation and any future SAP write‑back run under an "always ask" permission policy — the agent pauses and a human approves before anything changes state.
- **Per‑tenant isolation.** Each customer gets its own environment/vault and its own learned baselines and rule set. Agents in one tenant cannot see another's data.

## 3.5 The continuous loop (Study → Remodel → Apply)

The agents don't just run once — they implement the deck's improvement loop:

```
Study     → learn the expected, measure the actual, explain the deltas   (agents investigate)
Remodel   → tighten the expected, reshape policy, redesign the step       (humans ratify, baselines update)
Apply     → put the improved expected back into operation, then watch again
```

Fix, Govern, and Grow are this *same loop* run on errors, recurring patterns, and opportunities respectively. The correction population is the feedback signal: every credit memo the customer issues teaches the determination model to catch the next one earlier. **This is the compounding moat — the product is more valuable on day 500 than day 1.**

## 3.6 What you run, concretely, when you sell a deal

1. Get a scoped SAP extract → run the **Data‑Quality Agent** (readiness scorecard).
2. Run the **Mapping Agent** → confirm the config with the customer's SD process owner.
3. Run the **Behavior‑Study Agent** → produce the priced leakage report. **This is the close.**
4. On signature, stand up the customer tenant, pin the config, and turn on the **run‑time agents in observe mode**.
5. Review the first cases with the champion, tune thresholds, then graduate from observe → alert → (later) prevent.

See the full motion in [`06-gtm-deployment-playbook.md`](06-gtm-deployment-playbook.md).
