# 6 · Go‑to‑Market & Per‑Customer Deployment Playbook

The repeatable runbook for every customer you sell to. The whole point of the productization work is that this motion is the *same* each time, with only the configuration layer changing.

## 6.1 The motion (land → onboard → deploy → expand)

```
 LAND                 ONBOARD               DEPLOY                 EXPAND
 ───────────────────  ────────────────────  ─────────────────────  ─────────────────────
 Behavior Study       Map config            Tenant + observe mode   Govern + Grow editions
 (paid POC, priced    (Mapping Agent +      (run-time agents on,     (ratify rules, ROI,
  leakage report)      human ratify)         observe→alert→prevent)   maturity-curve upsell)
```

### Stage 1 — LAND: the Behavior Study (4–6 weeks, paid)

The deck *is* the pitch; the **Behavior Study** is how you prove it on the prospect's own data.

1. NDA + scoped, read‑only SAP extract (a sample of orders/items/conditions/billing/memos across a representative period).
2. Run the **Data‑Quality Agent** → readiness scorecard ("what we can study today").
3. Run the **Mapping Agent** → draft configuration; review ambiguous mappings with their SD process owner.
4. Run the **Behavior‑Study Agent** → the deliverable: a **priced leakage report** — top drivers, $ at stake, by segment/dealer/component, plus the "how much discount are we giving away?" view.
5. Present findings to the economic buyer. The report's own numbers (credit‑memo rate, leakage $, reinvoice rate) are the business case and the price anchor.

> First wave to show in the report (high value × feasible, ground truth available): **incentive coverage gaps, reinvoice root‑cause, fleet expected‑vs‑invoiced, discount give‑away, CFDI pre‑stamp.** Lead with whichever is biggest in *their* data.

### Stage 2 — ONBOARD: stand up the tenant

- Provision an isolated tenant (lakehouse namespaces, Postgres, agent environment/vault) via Terraform.
- Establish the production read‑only SAP connection (CDS/OData + CDC events); least‑privilege service account.
- Ratify and pin the **configuration** produced in Stage 1; pin agent versions.
- Load history to build initial baselines (dealer and fleet, separately).

### Stage 3 — DEPLOY: observe → alert → prevent

- Turn on the **run‑time agents in observe mode**. They produce cases without alerting anyone yet.
- Weekly review with the champion: tune thresholds, validate precision per flag type.
- Graduate each flag type **observe → alert** once precision clears the agreed bar, then later toward **prevent** (catch at entry). Never skip straight to alerting — false positives kill trust.
- Schedule the cadence agents (nightly reinvoice clustering, weekly governance discovery, monthly effectiveness).

### Stage 4 — EXPAND: climb the maturity curve

- Move the customer up `React → Catch → Prevent → Shape` and up the edition ladder `Protect → Protect+Comply → Grow`.
- Activate **Governance** (ratify high‑consistency rules into documented control; drift watch) — strong renewal/audit story.
- Activate **Grow** (incentive effectiveness, give‑away reduction, program‑ROI prediction) — net‑new revenue story, expands the buyer from OTC ops into the commercial org.

## 6.2 What you run at each step (agent checklist)

| Step | Agent(s) you run | Human action |
|------|------------------|--------------|
| POC | Data‑Quality → Mapping → Behavior‑Study | SME confirms mappings; buyer reviews report |
| Onboard | (config ratified, baselines built) | Ratify config, pin versions |
| Go‑live | Determination, Eligibility, Invoicing — observe | Champion reviews first cases |
| Cash | Reinvoicing Root‑Cause, Order‑Change | Fix top root causes |
| De‑risk | Compliance (MX/LATAM), Governance | Ratify first rules |
| Grow | Incentive‑Effectiveness | Redirect spend; plan programs |

## 6.3 Proof & value tracking (the renewal engine)

Track the deck's own measures per customer, before/after, and report them quarterly:

- **Protect:** credit‑memo rate, margin leakage $ recovered.
- **Cash:** reinvoice rate, DSO.
- **De‑risk:** CFDI exposure events caught, governance rules banked, audit findings.
- **Grow:** incremental volume attributable to programs, program ROI, give‑away reduction.

This dashboard *is* the renewal conversation and the value‑share invoice backup.

## 6.4 Risks & how the design mitigates them

| Risk | Mitigation (already in the design) |
|------|-----------------------------------|
| Long/painful SAP security review | Read‑only, advisory v1; no write‑back; least‑privilege; audit log; data residency |
| False positives erode trust | Observe→alert→prevent graduation; baseline confidence; $‑priced cases only |
| "It's just a dashboard" objection | Learns each segment's normal, discovers unqueried deltas, sharpens with corrections — agents, not rules |
| Customer‑specific SAP config | Configuration‑as‑data layer; Mapping Agent accelerates each onboarding |
| Agent cost on a continuous fleet | Haiku‑first triage, prompt caching of stable prefix, batch non‑interactive runs, token telemetry |
| Compliance/tax sensitivity (MX/SAT) | Dedicated Compliance Agent + auditable UUID‑linkage and reissue‑rate exposure tracking |
| Data leaving customer boundary | Per‑tenant isolation; self‑hosted sandbox option for tool execution inside the VPC |

## 6.5 The ask (how to frame the deal — straight from the deck)

> Protect the value pricing creates. Then use the same study to grow it. One behavior study across every price component and every phase — learning from the errors the process already produces. Start at determination and the discount give‑away; follow the lifecycle into reinvoicing, invoicing and compliance; then turn the same patterns toward governance you can bank and incentives that sell more.
