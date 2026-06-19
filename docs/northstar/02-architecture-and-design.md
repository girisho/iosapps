# 2 · Architecture & Design

## 2.1 System overview

```
        SAP (ECC / S/4HANA)                         NorthStar Platform
 ┌───────────────────────────┐        ┌────────────────────────────────────────────┐
 │ SD/OTC pricing             │        │                                              │
 │  • Sales orders, items     │  CDC / │  ┌────────────┐   ┌──────────────────────┐   │
 │  • Condition records       │ extract│  │ Ingestion  │──▶│ Lakehouse (bronze/   │   │
 │  • Condition contracts     │───────▶│  │ + mapping  │   │ silver/gold)         │   │
 │  • Billing docs VBRK/VBRP  │ (RFC/  │  └────────────┘   └──────────┬───────────┘   │
 │  • Change docs (Step 28…)  │  CDS/  │                              │               │
 │  • Credit/debit memos      │  IDoc) │              ┌───────────────▼────────────┐  │
 │  • CFDI/SAT (via PAC)      │        │              │  Expected-vs-Actual Engine  │  │
 └───────────────────────────┘        │              │  build EXPECTED · capture   │  │
                                       │              │  ACTUAL · score Δ           │  │
                                       │              └───────────────┬─────────────┘  │
                                       │                              │ deltas + cases │
                                       │   ┌──────────────────────────▼─────────────┐  │
                                       │   │  Agent Runtime (Claude Managed Agents)  │  │
                                       │   │  investigate · cluster · draft rules ·  │  │
                                       │   │  produce deploy-time analyses           │  │
                                       │   └──────────────────────────┬─────────────┘  │
                                       │   ┌──────────────────────────▼─────────────┐  │
                                       │   │  App layer: cases, governance workflow, │  │
                                       │   │  dashboards, alerts, reporting, API     │  │
                                       │   └─────────────────────────────────────────┘  │
                                       └────────────────────────────────────────────┘
```

**Design principles**

1. **Read‑mostly first.** Ingest and analyze; never write to SAP in v1. Write‑back (e.g., posting a flagged correction) is a later, opt‑in capability behind explicit approval.
2. **Configuration as data.** All SAP‑specific mappings are declarative config, validated against a schema — the universal engine never hard‑codes a Z‑condition.
3. **Segment‑aware everywhere.** Dealer (`ZVAAUI`) and fleet (`ZVAAFL`) are baselined *separately* — a blended baseline averages the errors away. Segmentation is a first‑class dimension in the data model, the engine, and the agents.
4. **Everything carries a dollar.** A delta without a $ value is noise. Every Δ surfaced is priced.
5. **The corrections are the ground truth.** Z601 credit memos, Z701 debit memos, DSR claims, manual journals — each is a labeled record of something that went wrong upstream. They are the supervised signal that makes "Detect" sharpen over time.

## 2.2 The Expected‑vs‑Actual engine (the core mechanic)

For each **price component** on each **transaction**, in each **lifecycle phase**, the engine computes:

```
EXPECTED  = f(peer orders, history, policy, cost-to-serve, segment, date window)
ACTUAL    = value observed in the SAP transaction
Δ (delta) = ACTUAL − EXPECTED, classified and priced
```

Δ is then routed three ways (the deck's "Fix / Govern / Grow"):

- **Fix** — deltas that are *mistakes* → caught before billing (a case).
- **Govern** — deltas that *recur and are right* → become candidate policy.
- **Grow** — the *pattern* of deltas → what to do better next.

### Component coverage (each is a study lens with a "what's at stake")

| Component | EXPECTED is built from | What AI studies | At stake |
|-----------|------------------------|-----------------|----------|
| **List price** | date/region/model consistency | base correctness by date/region/model | a wrong base cascades into every line |
| **Incentives & discounts** (SPA/eDeal, VPAS, programs) | expected coverage per dealer × series × country × date window; normal amount band | missing/wrong incentive, amount outside band | over‑concession, margin given away |
| **Eligibility & re‑determination** | SPA/program × class × model × dealer × geo × date; re‑trigger events | stale eligibility on Stock→Sold flips, lapsed programs | silent over/under‑credit |
| **Order changes & penalties** | normal change behavior per dealer; penalty triggers (G‑1873H) | churn/gaming patterns, unposted penalties | margin shift, rework |
| **Surcharges** | pass‑through coverage by material & period | un‑recovered surcharge | absorbed as cost |
| **Freight** | recovery rate by lane & dealer | under‑recovery | freight eats margin |
| **Warranty (SSP)** | pre/post‑invoice pricing consistency | mispriced obligations | margin & risk |
| **RAR** | allocation & recognition timing (606/IFRS15) | misallocation, timing | revenue misstatement, audit exposure |
| **Margin rollup** | sum across all levers, by segment | where & why margin leaks | the headline answer |

### How EXPECTED is actually computed

A layered approach — each "expected" is the strongest signal available for that component:

1. **Consistency / peer baselining** — for a given (segment, dealer, series, country, date window), what do *comparable* orders do? High agreement → strong expected (and a governance candidate). This is unsupervised and needs no labels.
2. **Policy/rule expected** — where a documented rule exists (program eligibility windows, surcharge schedules), expected = the rule's output.
3. **Supervised models** — trained on the correction population (credit memos, claims) to predict "this order will be corrected" from its entry signature.
4. **Statistical bands** — normal amount/rate distributions per condition per segment; flag out‑of‑band.

The engine stores **why** it expected what it expected (provenance), so every flag is explainable to a pricing analyst and to audit.

## 2.3 Data model (conceptual)

Medallion lakehouse:

- **Bronze** — raw SAP extracts, immutable, append‑only (orders, items, KONV/condition records, condition contracts, VBRK/VBRP, change docs, memos, CFDI events).
- **Silver** — conformed, segmented, joined into a **transaction‑lifecycle spine**: one row per (unit/VIN or order‑item) tracing entry → incentive determination → eligibility → pricing → changes → invoicing → reinvoicing, with the active segment and price‑component breakdown.
- **Gold** — the **Expected/Actual/Δ** facts per component, the priced cases, governance rule candidates, correction clusters, and the metrics marts (credit‑memo rate, leakage $, reinvoice rate, DSO, program ROI).

Key conformed dimensions: `segment`, `dealer`, `series/model`, `country/region`, `program/SPA`, `condition_type`, `lifecycle_phase`, `date_window`.

## 2.4 Segmentation (dealer vs. fleet)

| | Dealer (`ZVAAUI`) | Fleet (`ZVAAFL`) |
|--|-------------------|------------------|
| Shape | high volume, SPA/program‑driven | large, negotiated, multi‑unit |
| Dynamics | Stock↔Sold churn per unit; floor‑plan/BMI interest | Customer Expected Price carried natively; TOPS reconciliation; settled via accrual condition contracts |
| Typical error | missing/wrong incentive → DSR claim + credit memo | reconciliation gap on big deals (ZSPV/ZDIF Cust‑Exp‑Price drift) |

Baseline and alert on each independently.

## 2.5 Security, data & compliance design

- **Data minimization & residency.** Pull only the pricing/billing fields needed; support per‑region residency (esp. LATAM). PII is limited and tokenized where possible.
- **Read‑only SAP service account** with a constrained authorization profile; all extracts logged.
- **Tenant isolation.** Each customer is a logically isolated tenant (separate lakehouse namespaces, separate learned baselines and rule sets, separate agent vaults/credentials).
- **Auditability.** Every Δ, every ratified rule, every agent action is logged with provenance and is reproducible — this is also a *selling point* for Internal Audit and for the Mexico/SAT compliance module (UUID linkage, reissue‑rate as audit exposure).
- **No secrets in prompts.** Credentials for SAP, the data warehouse, and any MCP/tool integrations live in a secrets manager / agent vault, never in agent system prompts or messages.
- **Human‑in‑the‑loop by default.** Agents *recommend*; people *ratify* and *act*. Any state‑changing action (rule activation, future SAP write‑back) is gated behind explicit human approval.
