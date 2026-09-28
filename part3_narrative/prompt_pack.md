# Reusable Prompt Pack — Flagged Category Narrative

## Trigger

Start this prompt when a category's `is_flagged` result is `"flagged"`.

## Input list

The prompt requires these placeholder variables:

- `{category}` — category name
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — Month-on-Month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month

## Prompt

Write a concise stakeholder update for a regional manager about the flagged category.

Use the **Context → Insight → Implication** structure.

**Context:** State the category and the comparison period using `{month}` and `{prev_month}`. Mention the supplied revenue values `{previous_revenue}` and `{current_revenue}` when relevant.

**Insight:** State the Month-on-Month change using the exact supplied value `{mom_pct}` and explicitly label it as a **fact**.

**Implication:** Give one specific and actionable next step for the regional manager. If a possible cause is suggested but is not proven by the supplied data, label it explicitly as a **hypothesis**.

Use only the information supplied in the placeholders. Never invent or calculate any additional number, percentage, date, reseller name, or business fact. Never state a number that is not one of the supplied placeholder values.

## Checklist

Before using the narrative, verify:

1. Every number in the draft matches one of the supplied placeholder values exactly.
2. The category and comparison months match the supplied inputs.
3. Every factual observation is clearly presented as a fact, and any proposed cause is clearly labeled as a hypothesis.
4. The recommendation is specific and actionable rather than vague.
5. No raw reseller name or other internal identifier is exposed in an external-facing narrative.