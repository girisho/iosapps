# 1 · Product Strategy

## 1.1 What we are selling

**NorthStar** is an *Agentic Pricing Intelligence* layer that sits beside any SAP customer running condition‑technique pricing (SD/OTC), starting with commercial‑vehicle manufacturing (the "International" reference process in the deck) and generalizing to any condition‑technique pricing customer.

It is **read‑mostly and advisory**: NorthStar does not run pricing in SAP. It *studies* how pricing and invoicing behave, catches what breaks, ratifies what's consistent into governance, and recommends where to grow. This positioning is deliberate — it dramatically lowers the buyer's risk and shortens security review, because we never write back to the order on day one.

### The three sellable outcomes (one engine, three pitches)

| Mode | Buyer pain | What NorthStar delivers | Economic proof |
|------|-----------|--------------------------|----------------|
| **Detect / Protect** | Margin leaks silently — missing incentives, wrong nets, reinvoice churn | Flags the order/invoice that deviates from its segment's normal, *before billing*, with the $ gap attached | Credit‑memo rate ↓, margin leakage $ recovered |
| **Govern** | "Tribal" pricing rules nobody wrote down; audit exposure | Surfaces high‑consistency patterns, lets a human ratify them into documented, auditable control, flags drift | # rules banked, audit findings ↓ |
| **Grow** | Nobody can say which discount/program actually drove volume | Pairs incentive exposure with volume response; finds whitespace; predicts program ROI | Incremental volume, program ROI, give‑away reduced |

Sell **Protect first** (fast, measurable, low‑risk), then expand into Govern and Grow on the baseline the first phase creates. This is the land‑and‑expand spine of the whole business.

## 1.2 Who buys it

- **Economic buyer:** VP Order‑to‑Cash / VP Pricing / CFO org. They feel margin leakage and reinvoice rework directly.
- **Champion:** Pricing operations lead, revenue‑assurance lead, or SAP SD process owner.
- **Blockers to disarm early:** SAP Basis/Security (data access), Tax/Compliance (esp. Mexico CFDI/SAT), Internal Audit (governance), Data Privacy.

## 1.3 Productization arc — from one customer to a platform

The deck is grounded in one live OTC‑05 configuration. To make it a *product*, separate **what's universal** from **what's customer‑specific**:

```
┌─────────────────────────────────────────────────────────┐
│ UNIVERSAL PRODUCT (we build & own, versioned)            │
│  • Expected-vs-Actual engine & delta scoring             │
│  • Component model: list / incentive / surcharge /       │
│    freight / warranty(SSP) / RAR / margin rollup         │
│  • Agent runtime + agent library                         │
│  • Governance ratify/drift workflow                      │
│  • UI, alerting, case management, reporting              │
├─────────────────────────────────────────────────────────┤
│ CONFIGURATION LAYER (per customer, declarative — no code)│
│  • SAP table/condition-type mappings (ZA5U, table 917…)  │
│  • Segment definitions (dealer ZVAAUI vs fleet ZVAAFL)   │
│  • Lifecycle step mappings (Step 28, OTC_I023…)          │
│  • Compliance modules (Mexico CFDI/SAT, export Z201…)    │
├─────────────────────────────────────────────────────────┤
│ LEARNED LAYER (per customer, grows over time)            │
│  • Baselines of "normal" per segment × component         │
│  • Ratified governance rule set                          │
│  • Correction root-cause clusters                        │
└─────────────────────────────────────────────────────────┘
```

**Rule:** anything that references a customer's specific SAP object (a Z‑condition, a table number, a program code) lives in the *configuration layer* as data, never in code. This is what makes the engine "the same for any SAP pricing customer" while the examples stay real.

### Maturity / adoption curve (sell the journey)

`React (fix after billing) → Catch (flag at entry) → Prevent (stop upstream) → Shape (set pricing & grow).` Each customer climbs this curve; each step up is an upsell and a renewal story. The same engine that protects margin also moves the customer's *people* from finding problems to deciding what to do about them.

## 1.4 Packaging & pricing

- **Edition tiers** mapped to the maturity curve:
  - **Protect** — determination + invoicing study, observe mode, core components.
  - **Protect+Comply** — adds reinvoicing root‑cause + Mexico/LATAM compliance (CFDI/SAT, UUID linkage, export).
  - **Grow** — incentive effectiveness, give‑away analysis, program ROI, governance‑from‑consistency.
- **Pricing model:** annual platform subscription + value‑share or tiered by transaction volume / # of pricing components monitored. Anchor the price to recovered margin and reduced reinvoice rework (the deck's own measures: credit‑memo rate, margin leakage, reinvoice rate, DSO).
- **Land:** a paid "Behavior Study" engagement (4–6 weeks) that runs the engine on a data extract and produces a quantified leakage report. This *is* the sales motion and the first deliverable — see [`06-gtm-deployment-playbook.md`](06-gtm-deployment-playbook.md).

## 1.5 Where to start — first wave (value × feasibility)

From the deck's value/feasibility matrix, the first wave "picks itself" — high consistency, high impact, ground truth available:

**Do first:** incentive coverage gaps · reinvoice root‑cause · fleet expected‑vs‑invoiced · discount give‑away analysis · CFDI pre‑stamp checks.
**Build toward:** surcharge/freight recovery · govern‑from‑consistency · incentive effectiveness · RAR allocation checks · duplicate‑billing detection.

The "grow" plays and RAR build on the baseline the first wave creates — so sequence them after, never before.
