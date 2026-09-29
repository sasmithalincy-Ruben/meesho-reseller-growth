from growth_engine import mom_growth, is_flagged, validate_feed


def test_april_may_ethnic_wear():
    # Test 1: April → May Ethnic Wear
    growth = mom_growth(104520.77, 185107.61)
    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


def test_may_june_beauty_personal_care():
    # Test 2: May → June Beauty & Personal Care
    growth = mom_growth(35542.11, 37559.07)
    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


def test_exact_8_percent_boundary():
    # Test 3: Exact 8% boundary
    growth = mom_growth(100000, 108000)
    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"


def test_corrupted_feed():
    # Test 4: Corrupted feed
    valid, errors = validate_feed(
        "part2_engine/fixtures/corrupted_feed.csv"
    )

    assert valid is False

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_part1_feed():
    # Test 5: Valid Part 1 feed
    valid, errors = validate_feed(
        "part2_engine/fixtures/monthly_category_revenue.csv"
    )

    assert valid is True
    assert errors == []