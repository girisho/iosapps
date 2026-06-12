# NorthStar — Agentic Pricing Intelligence

> Productizing the "Agentic Pricing Intelligence" concept (OTC‑05 Order Management & Pricing) into a repeatable, sellable SAP‑pricing product.

This folder is the end‑to‑end product plan derived from the `NorthStar_Pricing_SAP` deck. It covers what we are building, how it is designed, the AI/agent architecture, the technology stack, the sprint‑by‑sprint build process, and the go‑to‑market motion for deploying it at each customer you sell to.

## Read in this order

| # | Doc | What it answers |
|---|-----|-----------------|
| 1 | [`01-product-strategy.md`](01-product-strategy.md) | What the product is, who buys it, how we go from one customer to a platform, pricing/packaging. |
| 2 | [`02-architecture-and-design.md`](02-architecture-and-design.md) | System design, the Expected‑vs‑Actual engine, data model, security & compliance. |
| 3 | [`03-agent-system.md`](03-agent-system.md) | The agents — what they are, how they run, and how you run them when you sell & deploy. |
| 4 | [`04-tech-stack.md`](04-tech-stack.md) | Concrete technology choices and why. |
| 5 | [`05-sprint-plan.md`](05-sprint-plan.md) | End‑to‑end delivery: phases, sprints, backlog, definition of done. |
| 6 | [`06-gtm-deployment-playbook.md`](06-gtm-deployment-playbook.md) | The repeatable "sell → onboard → deploy → expand" runbook per customer. |

## The one‑sentence thesis

> **We don't lack pricing data — we lack a view of what *should* have happened.** Build the *expected* price for every order and component, capture the *actual* from SAP, and the monitored gap (Δ) is the intelligence — used three ways: **Detect** errors before they cost, **Govern** the patterns the business already agrees on, and **Grow** revenue by measuring what actually moves volume.

## The product in four moving parts

1. **Ingestion** — read SAP OTC pricing data (condition records, condition contracts, billing docs, change docs) across the Order‑to‑Cash lifecycle, segmented dealer vs. fleet.
2. **The Engine** — for every price component (list, incentive, surcharge, freight, warranty/SSP, RAR) build *Expected* from peers/history/policy/cost‑to‑serve, compare to *Actual*, and surface the Δ with a dollar value attached.
3. **The Agents** — autonomous, model‑driven workers that investigate deltas, cluster correction root‑causes, draft governance rules, and produce the deploy‑time analyses you run when selling.
4. **The Loop** — Study → Remodel → Apply. Every correction the customer's process produces becomes new training signal, so the system sharpens the longer it runs.

## Why this is defensible (and not "just a dashboard")

A report counts the errors someone already predicted, using the same rules for dealer and fleet, and is as useful on day 500 as day 1. NorthStar learns each segment's *normal* on its own, discovers deltas nobody queried for, tells you which incentive moved volume vs. gave away margin, and gets better with every correction it ingests. That learning loop + the agent layer is the moat.
