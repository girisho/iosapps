# NorthStar Performance Assurance Strategy

This is the response pack for the VP IT request after the Oct 1, 2026 call: a plan to prove the NorthStar solution at production load before tech go-live on Dec 15, 2026. The solution covers S/4HANA 2023 FPS02 on RISE, the BTP Integration Suite, and Central Finance fed from Infor LN.

| File | What it is |
|---|---|
| `NorthStar_Performance_Assurance_Strategy.pptx` | A 20-slide deck in NorthStar brand style for VP IT and program leadership |
| `NorthStar_Performance_Assurance_Plan.xlsx` | The working tool, one tab each: plan with Gantt chart, RACI, scenario catalog, workload model, scaling model, KPI library, interface and batch inventories, environment readiness, risks and decisions, team |
| `graphics/*.svg` | Standalone diagrams: test architecture, timeline, risk-tier pyramid, 50% scaling model |
| `src/` | Generators for the graphics, deck and workbook |

## The strategy in one paragraph

Set up performance assurance as its own funded workstream, with an International owner and a dedicated specialist team. Replace "several hundred tests" with a risk-tiered scope:

- about 35 scripted Tier 1 end-to-end scenarios;
- about 70 Tier 2 component checks;
- telemetry for everything else.

Start baselining in SIT2 now; most go-live performance defects are in code. Execute in a protected pre-prod window from Nov 2 to Dec 4. Translate the results from the 50%-sized pre-prod with a three-class model:

- **Response time** does not scale with capacity.
- **Throughput** scales with capacity, but not linearly.
- **Fixed limits** (BTP tenant, JMS, Cloud Connector, number ranges, OneSource, PAC) are the same in pre-prod and production, so they must be tested at full load.

A formal performance go/no-go gate on Dec 4 feeds tech go-live readiness.

## Assumptions to validate

- Volumes, peak profiles and KPI thresholds are proposals until volumes are mined (Oct 14) and process owners sign the KPIs (Oct 23). Workload rows marked EXAMPLE contain illustrative values only.
- The SIT2 and Mock-2 end date is assumed. The pre-prod ratio of 0.5 comes from VP IT and should be replaced with the ECS configuration once it arrives.
- Check with SAP before relying on Going-Live Check entitlement or a temporary ECS upsize.
