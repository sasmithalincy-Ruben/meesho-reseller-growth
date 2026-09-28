# Part 4 — Agent Specification

## Goal

Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while ensuring every drafted message is held for human approval before it can be sent.

## Tools

The agent uses the following project functions:

- `validate_feed` — validates the monthly revenue CSV before any analysis begins.
- `mom_growth` — calculates Month-on-Month revenue growth.
- `is_flagged` — classifies the MoM result as `flagged`, `not_flagged`, or `escalate_exact_boundary`.
- Part 3 prompt-pack template-fill logic — creates a stakeholder narrative for flagged categories.

The Part 2 functions are imported and reused without re-implementing their logic.

## Memory / State

Between runs, the agent must retain the previous month's revenue for each category so that the next run can calculate the category's Month-on-Month change.

The current month's validated revenue becomes the previous-month reference for the subsequent run.

## Planner

The agent executes these subtasks in order:

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, Hard Stop and report all validation errors.
3. If validation succeeds, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` in descending order.
6. Draft a stakeholder message for at most the top 3 flagged categories using the Part 3 prompt template.
7. Log any remaining flagged categories beyond the top-3 cap as `suppressed, review manually` without drafting a message.
7b. Separately log every category whose result is `escalate_exact_boundary` in `escalated_categories` without drafting a message.
8. Emit one structured JSON object for the run.

## Feedback Loop

No message is automatically sent.

Every drafted message is held for human approval. The runner represents this by returning the action status:

`drafted_and_held_for_approval`

The human approval checkpoint must occur before any message is considered sent.

## Guardrails

### Input Guardrail

`validate_feed` must pass before any growth calculation, flagging, sorting, or drafting occurs.

If validation returns `False`, the agent performs a Hard Stop and surfaces the validation errors.

### Action Guardrail

No message is ever automatically sent. The agent only drafts messages and holds them for human approval.

### Output Guardrail

Every number in a drafted message must trace back to a supplied Part 1 or Part 2 value. The agent must not invent additional figures.

## Success and Error Stopping Conditions

### Success

A successful run produces the required structured output with drafted messages for the top three flagged categories, or correctly produces zero drafted messages when no category crosses the threshold.

Every number in each drafted message must be traceable to the supplied verified data.

### Error

If `validate_feed` returns `False`, the run is a **Hard Stop**.

The validation errors must be surfaced in `validation_errors`, no MoM computation is attempted, and no messages are drafted.

## Given-When-Then Agent Specifications

### 1. April → May Ethnic Wear

**GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61,  
**WHEN** the agent computes `mom_growth` and then applies `is_flagged`,  
**THEN** `mom_growth` returns `77.1` and `is_flagged` returns `"flagged"`.

### 2. May → June Beauty & Personal Care

**GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07,  
**WHEN** the agent evaluates the category,  
**THEN** `mom_growth` returns `5.67` and `is_flagged` returns `"not_flagged"`.

### 3. Exact 8% Boundary

**GIVEN** a synthetic pair with `previous=100000` and `current=108000`,  
**WHEN** the agent evaluates the category,  
**THEN** `mom_growth` returns exactly `8.0` and `is_flagged` returns `"escalate_exact_boundary"`.

### 4. Corrupted Feed

**GIVEN** the corrupted feed fixture,  
**WHEN** the agent runs `validate_feed`,  
**THEN** validation returns `False` with exactly these three errors in order:

1. `line 3: negative revenue (-4200.0) for category=Western Wear`
2. `line 4: missing category (month=July)`
3. `line 6: missing revenue (category=Home & Kitchen)`

The agent performs a Hard Stop and does not perform MoM computation.