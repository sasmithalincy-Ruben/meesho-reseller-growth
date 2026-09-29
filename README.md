# Meesho Reseller Growth Analysis & Guarded Agent Workflow

## Project Overview

This project builds an end-to-end, guarded workflow for monitoring Meesho reseller category revenue changes.

The project combines SQL analysis, Python validation and growth detection, reliable narrative generation, data masking, and a mock agent workflow into one repeatable pipeline.

The complete pipeline runs locally with **zero API keys, zero paid services, and no external API calls**.

---

## Project Structure

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── queries.sql
├── run_queries.py
├── run_query2.py
├── run_query3.py
├── run_query4.py
├── run_query5.py
└── output/

part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/

part3_narrative/
├── prompt_pack.md
├── narrative_report.md
├── masking.py
└── test_masking.py

part4_agent/
├── agent_spec.md
├── mock_agent_runner.py
├── test_mock_agent_runner.py
└── fixtures/
```

---

## Requirements

Run the project from the repository root.

Python 3 is required.

Install pytest if it is not already available:

```bash
python -m pip install pytest
```

No API key or external account is required.

---

# Running the Complete Pipeline

Run the Parts in the following order:

```text
Dataset
   ↓
Part 1 – SQL Business Analysis
   ↓
Part 2 – Validation + MoM Growth Detection
   ↓
Part 3 – Narrative + Data Masking
   ↓
Part 4 – Guarded Agent Workflow
```

---

## Step 1 – Regenerate the Dataset

Run:

```bash
python data/generate_dataset.py
```

This generates the reseller data, order data, and SQLite database used by the project.

The generated data is stored in:

```text
data/resellers.csv
data/orders.csv
data/meesho_reseller.db
```

---

# Part 1 – SQL Business Analysis

Part 1 uses SQL to calculate verified business metrics from the project database.

Run:

```bash
python part1_sql/run_queries.py
python part1_sql/run_query2.py
python part1_sql/run_query3.py
python part1_sql/run_query4.py
python part1_sql/run_query5.py
```

The generated CSV outputs are stored in:

```text
part1_sql/output/
```

Part 1 produces business analysis such as:

* Monthly category revenue
* Region-wise revenue
* Top resellers
* Resellers with no orders
* Average order value

The SQL output provides the verified business numbers used by the downstream workflow.

---

# Part 2 – Python Growth Engine

Part 2 validates the monthly revenue feed and calculates month-on-month revenue growth.

Run the tests:

```bash
python -m pytest part2_engine/test_growth_engine.py
```

The growth engine uses:

```text
validate_feed
mom_growth
is_flagged
```

The flagging threshold is 8%.

Categories whose month-on-month movement crosses the defined threshold are flagged. The exact 8% boundary is handled separately as an escalation case.

Part 2 prevents invalid input data from reaching the growth-detection stage.

---

# Part 3 – Reliable Narrative and Data Masking

Part 3 converts verified growth results into stakeholder-friendly narratives.

Run the masking tests:

```bash
python -m pytest part3_narrative/test_masking.py
```

Part 3 contains:

```text
prompt_pack.md
narrative_report.md
masking.py
test_masking.py
```

The narrative uses the:

```text
Context → Insight → Implication
```

structure.

The masking policy prevents raw reseller names from appearing in external-facing narratives and replaces reseller identifiers with coded aliases.

The narrative process is deterministic and fully offline. It does not require an AI API or API key.

---

# Part 4 – Guarded Mock Agent Workflow

Part 4 combines the previous parts into a repeatable monitoring workflow.

Run the Part 4 tests:

```bash
python -m pytest part4_agent/test_mock_agent_runner.py
```

The mock agent performs these steps:

1. Load the monthly revenue feed.
2. Validate the input feed.
3. Hard Stop if validation fails.
4. Calculate month-on-month growth for each category.
5. Apply the flagging rule.
6. Sort flagged categories by absolute growth percentage.
7. Draft messages for at most the top three flagged categories.
8. Suppress additional flagged categories for manual review.
9. Record exact-boundary escalation cases separately.
10. Return one structured JSON result for the run.

The agent **does not send emails or messages**.

Every drafted message is held for human approval.

---

# How the Parts Connect

## Part 1 → Part 2

Part 1 first computes verified business numbers using SQL.

Part 2 then validates the monthly revenue feed and calculates month-on-month growth from the verified revenue data.

```text
Raw Data
   ↓
Part 1 SQL Analysis
   ↓
Verified Revenue Numbers
   ↓
Part 2 Validation + Growth Detection
```

This follows the required **"compute real numbers via SQL first, then hand off"** order of operations.

---

## Part 2 → Part 3

Part 2 identifies categories whose revenue movement crosses the defined threshold.

Part 3 takes those verified results and turns them into a stakeholder-readable narrative using the Context → Insight → Implication structure.

```text
Part 2 Growth Result
   ↓
Part 3 Narrative Template
   ↓
Validated Narrative
   ↓
Masked Reseller Information
```

No unsupported numbers are invented in the narrative.

---

## Part 2 + Part 3 → Part 4

Part 4 orchestrates the earlier components into one guarded workflow.

It imports the Part 2 validation and growth functions and uses the Part 3 narrative structure for drafting.

```text
Intake
   ↓
Validate
   ↓
Compute
   ↓
Detect
   ↓
Prioritize
   ↓
Draft Report
   ↓
Validate Output
   ↓
Hold for Human Approval
```

This mirrors an **Intake → Summary → Report Draft → Validate** reporting flow.

---

# Guardrails

The pipeline uses three main guardrails.

### Input Guardrail

`validate_feed` must pass before growth calculations are performed.

If validation fails, the agent performs a **Hard Stop** and surfaces the validation errors.

### Action Guardrail

The agent never automatically sends a message.

It only creates a draft and holds it for human approval.

### Output Guardrail

Every number in a drafted message must trace back to the verified Part 1 or Part 2 data.

No invented figures are allowed.

---

# Testing

The project contains tests for Parts 2, 3, and 4.

Run them individually:

```bash
python -m pytest part2_engine/test_growth_engine.py
```

```bash
python -m pytest part3_narrative/test_masking.py
```

```bash
python -m pytest part4_agent/test_mock_agent_runner.py
```

Or run all project tests together:

```bash
python -m pytest
```

A successful run should report all tests as passing.

---

# Zero API Keys and Offline Execution

The entire project works with:

* Zero API keys
* Zero paid services
* No hosted AI service
* No external API calls
* No Gmail integration
* No SMTP integration
* No real message-sending integration

The AI narrative stage is implemented as a deterministic offline template-fill workflow.

Part 4 is a mock agent runner that drafts and holds messages for human approval rather than sending them.

---

# Academic Integrity / Documentation

The implementation uses Python standard-library functionality and local project files.

No external AI API is required to execute the pipeline.

---

# End-to-End Summary

The complete project follows this workflow:

```text
Dataset Generation
        ↓
Part 1 – SQL Business Analysis
        ↓
Verified Business Numbers
        ↓
Part 2 – Feed Validation + MoM Growth Detection
        ↓
Flagged Categories
        ↓
Part 3 – Reliable Narrative + Data Masking
        ↓
Part 4 – Guarded Agent Workflow
        ↓
Draft Message
        ↓
Human Approval Required
```

The result is a repeatable, locally executable, guarded business-monitoring pipeline that connects SQL analysis, Python validation, narrative generation, masking, and agentic workflow orchestration.
