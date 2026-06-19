# 4 · Technology Stack

Choices optimize for: enterprise SAP integration, a lakehouse that can hold years of pricing transactions, an agent runtime that's production‑grade, and a security posture that survives a manufacturing customer's review.

## 4.1 Stack at a glance

| Layer | Choice | Why |
|-------|--------|-----|
| **SAP ingestion** | SAP CDC via **OData/CDS extraction**, RFC/BAPI for table reads, IDoc for billing/memo events; landed by Fivetran/Airbyte **or** a thin custom extractor | Meet the customer's existing SAP integration standard; CDS views are the modern, supported path on S/4HANA |
| **Streaming / CDC transport** | Kafka (or cloud‑native: Kinesis / Pub/Sub) | Near‑real‑time order/billing events for observe‑mode flagging |
| **Lakehouse** | **Databricks** or **Snowflake** (Delta/Iceberg), medallion (bronze/silver/gold) | Years of transactions, cheap storage, SQL + ML in one place, per‑tenant isolation via schemas/catalogs |
| **Transformations** | **dbt** for silver/gold; Spark for heavy joins | Declarative, testable, version‑controlled transforms; configuration mappings expressed as dbt vars/seeds |
| **Expected‑vs‑Actual engine** | Python services (pandas/Polars + scikit‑learn / statistical baselines); feature store for learned baselines | Mix of unsupervised consistency baselining, statistical bands, and supervised correction‑prediction models |
| **Agent runtime** | **Claude Managed Agents** on the Claude Developer Platform | Anthropic runs the agent loop + per‑session sandbox; persisted/versioned agents; scheduled deployments; vaults for credentials; outcomes for rubric‑graded deliverables |
| **Reasoning model** | **`claude-opus-4-8`** (default) for investigation/clustering/rule‑drafting; **`claude-haiku-4-5`** for cheap high‑volume triage; **`claude-fable-5`** only for the hardest long‑horizon analyses | Opus 4.8 is the most capable Opus‑tier model for long‑horizon agentic work; Haiku for cost‑sensitive fan‑out; see §4.3 |
| **Backend / API** | Python (**FastAPI**) services; the orchestrator that hosts custom tools and holds credentials | First‑class Anthropic SDK; same language as the engine |
| **Case / workflow store** | Postgres (cases, governance rules, ratification state, audit log) | Transactional, auditable, relational workflow |
| **Frontend** | **TypeScript + React** (Next.js); component‑driven dashboards, case review, governance ratify/drift UI | Standard, fast, good charting ecosystem |
| **Infra** | Containers on Kubernetes (EKS/GKE) or the customer's preferred cloud; IaC via Terraform | Repeatable per‑tenant deploys |
| **Secrets** | Cloud secrets manager + Managed‑Agents vaults | No credential ever enters a prompt or sandbox |
| **Observability** | OpenTelemetry traces, structured logs, agent token/usage telemetry; dashboards in Grafana/cloud‑native | Cost control + auditability of agent actions |

## 4.2 Why Managed Agents (vs. rolling our own loop)

- Anthropic runs the agent loop *and* hosts the per‑session container where tools execute — we don't operate that compute.
- **Persisted, versioned agents** map exactly to our "build the agent once, deploy to every customer" model; pin a customer to a version, roll forward safely.
- **Scheduled deployments** give us the nightly/weekly/monthly cadence the run‑time agents need with no extra scheduler to babysit.
- **Vaults + custom tools** keep SAP/warehouse credentials host‑side and out of prompts — critical for the security review.
- **Outcomes** give the Behavior‑Study and report agents a rubric‑graded "done."
- For tenants that mandate self‑hosted compute (no data leaves their VPC for tool execution), Managed Agents supports **self‑hosted sandboxes** — the agent loop stays on Anthropic's side, but bash/file/code tools run on infrastructure we control inside the customer boundary.

> If a customer forbids the managed runtime entirely, the fallback is **Claude API + tool use** with our own orchestration loop — same models, same tools, we run the loop. Keep the tool definitions runtime‑agnostic so we can switch without rewriting the agents.

## 4.3 Model selection & cost discipline

- **Default reasoning:** `claude-opus-4-8` — most capable Opus‑tier model; best for the long‑horizon investigation, correction clustering, and rule drafting that are the high‑value agent work. Run agentic work at **`high`/`xhigh` effort** with the full task spec given up front.
- **High‑volume triage / fan‑out:** `claude-haiku-4-5` for the cheap first pass over thousands of orders (is this even worth a deeper look?), escalating only the interesting ones to Opus. This is the main cost lever.
- **Hardest analyses only:** `claude-fable-5` for the most demanding long‑horizon work, when justified — it's priced above Opus‑tier, so reserve it.
- **Prompt caching:** the per‑customer system prompt + config + tool definitions are a large, stable prefix shared across every session — cache it. This is a major cost reduction on a continuously‑running fleet of agents.
- **Batch where latency doesn't matter:** nightly reinvoice clustering and monthly effectiveness runs can use the Batches API (50% cheaper) for the bulk LLM calls that aren't interactive.
- **Token telemetry per tenant** feeds both cost control and the value‑share pricing story.

> Model IDs are exact strings (`claude-opus-4-8`, `claude-haiku-4-5`, `claude-fable-5`) — no date suffixes. Use adaptive thinking; do not use deprecated `budget_tokens`.

## 4.4 Build vs. buy

- **Buy/standardize:** SAP extraction connectors, lakehouse, dbt, the agent runtime, secrets manager — don't reinvent these.
- **Build (the IP):** the Expected‑vs‑Actual engine, the component model, the agent library + tools, the governance ratify/drift workflow, and the configuration schema that makes one engine serve many SAP customers. This is the product.
