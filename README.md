# Meesho Reseller Growth Analysis & Guarded Agent Workflow

## Project Overview

This project builds an end-to-end, guarded workflow for monitoring reseller category revenue changes.

The workflow moves through:

1. SQL-based business analysis
2. Python validation and growth detection
3. Reliable narrative generation and data masking
4. A mock agent workflow that combines the previous parts

The complete pipeline runs locally without external APIs or API keys.

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