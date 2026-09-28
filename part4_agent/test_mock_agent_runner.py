from pathlib import Path

from mock_agent_runner import run


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = PROJECT_ROOT / "part4_agent" / "fixtures"

APRIL = FIXTURES / "april.csv"
MAY = FIXTURES / "may.csv"
JUNE = FIXTURES / "june.csv"

CORRUPTED = (
    PROJECT_ROOT
    / "part2_engine"
    / "fixtures"
    / "corrupted_feed.csv"
)


def test_may_scenario():
    # GIVEN April -> May data
    result = run("May", str(APRIL), str(MAY))

    # WHEN the agent runs
    # THEN exactly the top 3 flagged categories are drafted
    assert result["validation_status"] == "valid"
    assert result["action_taken"] == "drafted_and_held_for_approval"

    flagged = result["flagged_categories"]

    assert len(flagged) == 3

    assert [item["category"] for item in flagged] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in flagged] == [
        77.1,
        -23.6,
        -23.48,
    ]

    assert all(item["drafted"] is True for item in flagged)

    assert set(result["suppressed_categories"]) == {
        "Beauty & Personal Care",
        "Home & Kitchen",
    }

    assert result["escalated_categories"] == []


def test_june_scenario():
    # GIVEN May -> June data
    result = run("June", str(MAY), str(JUNE))

    # WHEN the agent runs
    # THEN exactly the top 3 flagged categories are drafted
    assert result["validation_status"] == "valid"
    assert result["action_taken"] == "drafted_and_held_for_approval"

    flagged = result["flagged_categories"]

    assert len(flagged) == 3

    assert [item["category"] for item in flagged] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in flagged] == [
        -58.74,
        42.59,
        23.9,
    ]

    assert all(item["drafted"] is True for item in flagged)

    assert result["suppressed_categories"] == [
        "Western Wear"
    ]

    assert result["escalated_categories"] == []

    # Beauty & Personal Care is only 5.67%, so it must not appear.
    assert "Beauty & Personal Care" not in result["suppressed_categories"]
    assert "Beauty & Personal Care" not in [
        item["category"] for item in flagged
    ]


def test_corrupted_feed_hard_stop():
    # GIVEN the corrupted feed
    result = run("July", str(MAY), str(CORRUPTED))

    # WHEN validation fails
    # THEN the agent must hard stop
    assert result["validation_status"] == "invalid"
    assert result["action_taken"] == "hard_stop"

    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == []


def test_drafted_messages_contain_required_values():
    # GIVEN April -> May
    result = run("May", str(APRIL), str(MAY))

    # THEN every drafted message contains its category and exact MoM value
    for item in result["flagged_categories"]:
        message = item["message"]

        assert item["category"] in message
        assert str(item["mom_pct"]) in message


def test_required_top_level_keys():
    # GIVEN a valid May run
    result = run("May", str(APRIL), str(MAY))

    # THEN exactly the required JSON keys exist
    assert set(result.keys()) == {
        "run_month",
        "validation_status",
        "validation_errors",
        "flagged_categories",
        "suppressed_categories",
        "escalated_categories",
        "action_taken",
    }


print("All Part 4 tests passed!")