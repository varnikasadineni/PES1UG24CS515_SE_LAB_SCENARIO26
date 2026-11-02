import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate

# Goal: make every DECISION in loan_eligibility.py go both True and False,
# and test the boundary values where each decision flips.


# ---------- starter tests ----------
def test_excellent_band():
    assert credit_band(800) == "excellent"


def test_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True


# ---------- credit_band ----------
def test_score_below_range_raises():
    with pytest.raises(ValueError):
        credit_band(299)


def test_score_above_range_raises():
    with pytest.raises(ValueError):
        credit_band(901)


@pytest.mark.parametrize("score, band", [
    (300, "poor"),        # lowest valid score
    (549, "poor"),        # just below fair
    (550, "fair"),        # fair boundary
    (649, "fair"),
    (650, "good"),        # good boundary
    (749, "good"),
    (750, "excellent"),   # excellent boundary
    (900, "excellent"),   # highest valid score
])
def test_credit_band_boundaries(score, band):
    assert credit_band(score) == band


# ---------- is_eligible ----------
def test_unknown_employment_raises():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)


@pytest.mark.parametrize("age, expected", [
    (20, False),   # age < 21 is True
    (21, True),    # lower age boundary
    (60, True),    # upper age boundary
    (61, False),   # age > 60 is True
])
def test_age_limits(age, expected):
    assert is_eligible(age, 50000, "salaried", 800) is expected


@pytest.mark.parametrize("income, employment, expected", [
    (24999, "salaried", False),
    (25000, "salaried", True),
    (39999, "self_employed", False),
    (40000, "self_employed", True),
])
def test_income_limits(income, employment, expected):
    assert is_eligible(30, income, employment, 800) is expected


def test_poor_credit_not_eligible():
    assert is_eligible(30, 50000, "salaried", 549) is False


def test_fair_credit_eligible():
    assert is_eligible(30, 50000, "salaried", 550) is True


# ---------- interest_rate ----------
@pytest.mark.parametrize("score, employment, collateral, rate", [
    (800, "salaried",      False, 8),
    (800, "salaried",      True,  6),
    (800, "self_employed", False, 9),
    (800, "self_employed", True,  7),
    (700, "salaried",      False, 10),
    (700, "self_employed", True,  9),
    (600, "salaried",      False, 13),   # fair  -> else branch
    (400, "self_employed", False, 14),   # poor  -> else branch
])
def test_interest_rate_combinations(score, employment, collateral, rate):
    assert interest_rate(score, employment, collateral) == rate


def test_interest_rate_invalid_score_raises():
    with pytest.raises(ValueError):
        interest_rate(950, "salaried", False)
