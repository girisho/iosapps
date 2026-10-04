# Incident Lens

Explains SAP support incidents (SAP for Me → case → Print → Save as PDF) to people who aren't SAP specialists.

| File | What it is |
|---|---|
| `index.html` | Published as a claude.ai artifact. AI explanation built in; incidents and action-item ticks are shared with everyone who can open the page. |
| `standalone/incident-lens.html` | Same page as one file (PDF reader embedded, works offline). Incidents are kept in that browser; AI works by copying the prompt into Claude or Joule and pasting the answer back. |

## What it shows per incident

- **In plain words**: summary, analogy, business impact, where it stands, root-cause status, best next step, measured warning signals.
- **Clock and ownership**: live countdown to SAP's estimated automatic confirmation date, share of the response window used, who had the ball (from the action log), SAP teams the case passed through.
- **Recommended vs done**: SAP's recommendations with status (implemented, already done, pending, superseded…) next to what the project did; SAP Notes with links.
- **Disagreements**: each point with SAP's and the project's position side by side.
- **What to do next**: owned, prioritised action items with ticks; what SAP asked for last; a draft reply.
- **Conversation**: every message, filterable by SAP / project / system, new messages flagged on re-upload.
- **Glossary**: SAP terms in the case, explained.

Facts (dates, countdown, ownership, hand-offs, repeated advice, silences) are measured from the PDF without AI. The narrative sections come from AI and are labelled as such.

## Privacy

The PDF is read in the browser. Phone numbers, e-mail domains and meeting links/passcodes are masked before anything is stored or sent to AI.
