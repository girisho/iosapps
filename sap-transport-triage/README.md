# Transport Import Triage

Tools that help the Basis team find the root cause when an S/4HANA transport import ends with RC 8. The first use case is OTC condition tables (post-import method `RV_COND_TABLE_GEN_ACT_METHOD`, object `VKOS`).

| File | What it is | Where it runs |
|---|---|---|
| `index.html` | Learning log triage (published as a claude.ai artifact) with two sections: **S/4HANA transports** (tp/STMS/SE11 logs) and **BTP Cloud Transport** (Cloud Transport Management action logs; Integration Suite via Content Agent now, MTA/CAP apps next). Five stages: read any tp step log, explain step and RC, match against the team's knowledge base and built-in rules, let the user decide on unknown errors (ask AI, mark as noise, or write the rule), and remember the approved rule and the case. Team rules and case history live in the artifact's shared store. | claude.ai artifact; logs are parsed in the browser |
| `standalone/transport-import-triage.html` | The same tool as one self-contained file (Excel reader embedded, works offline). Opens in any browser. Rules and cases are kept in that browser; share them with Knowledge base → Export / Import. AI help works by copying the prompt into Claude or Joule and pasting the answer back. | Any browser, no claude.ai needed |
| `abap/zbc_cond_table_precheck.abap` | ABAP report that checks condition tables in the system directly: more than 16 key fields, fields missing from `KOMG`, inactive data elements, inactive table versions. ALV output. | DEV before release; QAS/PRD after a failed import |

## Recommended operating model

1. **Prevent it in DEV.** Run `ZBC_COND_TABLE_PRECHECK` before releasing pricing requests. To enforce it, move `lcl_check` into a global class and call it from an implementation of BAdI `CTS_REQUEST_CHECK`, method `CHECK_BEFORE_RELEASE`. Raise `CANCEL` when a table in the request returns an `ERROR` row.
2. **Diagnose fast in QAS.** When an import returns RC 8, drop `/usr/sap/trans/log/<SID>R<nr>.<target>` and the SE11 activation logs into `index.html`. The verdict, the fix steps and the ticket text are ready in about a minute.
3. **Keep learning.** Unknown errors are diagnosed with AI only when someone chooses to, reviewed, and approved into the shared knowledge base, so the next occurrence is recognised without AI. Recurring dictionary patterns can also become checks in the ABAP class.

## Case DS4K904917 → QS4 (2026-10-03)

- 194 condition tables processed: 175 activated, 19 failed, RC 8.
- A9HU: 17 key fields (MANDT, KAPPL, KSCHL, KFRST, DATBI plus 12 variable fields). The dictionary limit is 16, so the table can't be activated in any system. It has to be redesigned in DS4 with 11 or fewer variable fields.

## Case cTMS action 14576 → IntegrationSuite-QA (2026-09-29)

- Integration Suite package CPACIntegrationWithSAPS4HANA, deployed through Content Agent service; status 8.
- Cloud Integration returned `UniquenessViolationException`: a package or artifact with the same ID already exists in the QA tenant (typically the same artifact ID in another package, or a package imported or copied outside cTMS).
- The request was forwarded to IntegrationSuite-PREPROD before the QA import ran, so the failed content is already in that queue.
