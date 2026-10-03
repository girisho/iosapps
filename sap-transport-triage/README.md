# Transport Import Triage

Tools that help the Basis team find the root cause when an S/4HANA transport import ends with RC 8. The first use case is OTC condition tables (post-import method `RV_COND_TABLE_GEN_ACT_METHOD`, object `VKOS`).

| File | What it is | Where it runs |
|---|---|---|
| `index.html` | Browser log analyzer. Drop the import log and SE11 activation logs (xlsx export or text). It lists failed objects, picks the root cause, filters out namespace noise, counts condition-table key fields, and drafts the ticket text. An optional "Ask Claude" panel covers messages the rules don't recognise. | Any browser; nothing is uploaded |
| `abap/zbc_cond_table_precheck.abap` | ABAP report that checks condition tables in the system directly: more than 16 key fields, fields missing from `KOMG`, inactive data elements, inactive table versions. ALV output. | DEV before release; QAS/PRD after a failed import |

## Recommended operating model

1. **Prevent it in DEV.** Run `ZBC_COND_TABLE_PRECHECK` before releasing pricing requests. To enforce it, move `lcl_check` into a global class and call it from an implementation of BAdI `CTS_REQUEST_CHECK`, method `CHECK_BEFORE_RELEASE`. Raise `CANCEL` when a table in the request returns an `ERROR` row.
2. **Diagnose fast in QAS.** When an import returns RC 8, drop `/usr/sap/trans/log/<SID>R<nr>.<target>` and the SE11 activation logs into `index.html`. The verdict, the fix steps and the ticket text are ready in about a minute.
3. **Keep learning.** Each new failure pattern becomes a rule in the `KB` array in `index.html`, and a check in the ABAP class if it can be detected from the dictionary.

## Case DS4K904917 → QS4 (2026-10-03)

- 194 condition tables processed: 175 activated, 19 failed, RC 8.
- A9HU: 17 key fields (MANDT, KAPPL, KSCHL, KFRST, DATBI plus 12 variable fields). The dictionary limit is 16, so the table can't be activated in any system. It has to be redesigned in DS4 with 11 or fewer variable fields.
