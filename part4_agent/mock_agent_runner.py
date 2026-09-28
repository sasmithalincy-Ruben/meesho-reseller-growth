import csv
import json
import sys
from pathlib import Path

# Allow the runner to import Part 2 functions
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "part2_engine"))

from growth_engine import validate_feed, mom_growth, is_flagged


def load_feed(csv_path):
    """Load category revenue data from a CSV file."""
    rows = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def draft_message(
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    month,
    prev_month,
):
    """Create a stakeholder draft using the Part 3 narrative structure."""

    return (
        f"Context: {category} revenue is being compared for "
        f"{month} versus {prev_month}. "
        f"Previous revenue was {previous_revenue} and current revenue was "
        f"{current_revenue}. "
        f"Insight — Fact: {category} revenue changed by {mom_pct}% "
        f"from {prev_month} to {month}. "
        f"Implication — Hypothesis: The regional manager should review "
        f"the category's product availability, reseller activity, and "
        f"promotional factors to identify possible drivers of the change."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Run the guarded mock agent workflow."""

    # ---------------------------------------------------------
    # 1. Validate the current feed before doing anything else
    # ---------------------------------------------------------

    is_valid, validation_errors = validate_feed(current_month_csv)

    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # ---------------------------------------------------------
    # 2. Load both feeds
    # ---------------------------------------------------------

    previous_rows = load_feed(previous_month_csv)
    current_rows = load_feed(current_month_csv)

    previous_data = {
        row["category"]: float(row["revenue"])
        for row in previous_rows
    }

    current_data = {
        row["category"]: float(row["revenue"])
        for row in current_rows
    }

    # Previous month name comes from the CSV data.
    previous_month = previous_rows[0]["month"]

    flagged = []
    suppressed = []
    escalated = []

    # ---------------------------------------------------------
    # 3 & 4. Calculate MoM and classify every category
    # ---------------------------------------------------------

    for category, current_revenue in current_data.items():

        previous_revenue = previous_data[category]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        status = is_flagged(mom_pct)

        if status == "flagged":
            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
                "drafted": False,
            })

        elif status == "escalate_exact_boundary":
            escalated.append(category)

    # ---------------------------------------------------------
    # 5. Sort flagged categories by absolute MoM magnitude
    # ---------------------------------------------------------

    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # ---------------------------------------------------------
    # 6 & 7. Draft only the top 3
    # ---------------------------------------------------------

    for index, item in enumerate(flagged):

        if index < 3:

            item["drafted"] = True

            item["message"] = draft_message(
                category=item["category"],
                previous_revenue=item["previous_revenue"],
                current_revenue=item["current_revenue"],
                mom_pct=item["mom_pct"],
                month=month,
                prev_month=previous_month,
            )

        else:
            suppressed.append(item["category"])

    # ---------------------------------------------------------
    # 8. Return one structured JSON-compatible object
    # ---------------------------------------------------------

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged[:3],
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":

    print("Mock Agent Runner loaded successfully.")