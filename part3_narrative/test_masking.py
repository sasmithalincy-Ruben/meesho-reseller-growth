from masking import alias_for, assert_no_raw_names_leak


# Test alias creation
assert alias_for("RS019") == "ALIAS-19"
assert alias_for("RS006") == "ALIAS-06"


# Real reseller names from Part 1
reseller_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]


# Negative case: raw name must be detected
raw_text = "West region: Mumbai Reseller 1 generated revenue."

assert (
    assert_no_raw_names_leak(raw_text, reseller_names)
    is False
)


# Positive case: aliases are safe
masked_text = """
West region: ALIAS-19 generated total spend of INR 75295.09.
West region: ALIAS-22 generated total spend of INR 73882.33.
South region: ALIAS-12 generated total spend of INR 69936.46.
North region: ALIAS-06 generated total spend of INR 64238.97.
North region: ALIAS-05 generated total spend of INR 61825.020000000004.
"""

assert (
    assert_no_raw_names_leak(masked_text, reseller_names)
    is True
)


print("All Part 3 masking tests passed!")