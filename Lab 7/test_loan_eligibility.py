"""
Lab 7 - Fuzz testing loan_eligibility.py with Hypothesis.

Each function gets:
  1. a "no crash" fuzz test on completely random input (text or None), and
  2. targeted fuzz tests that build *almost valid* inputs, which reach the
     deeper edge cases (zero rate, huge numbers, bad PAN letters, etc.)
     that plain random text rarely hits.
"""
from hypothesis import given, settings, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES

# Random junk: any unicode text, None, or a non-string type
anything = st.text() | st.none() | st.integers() | st.floats() | st.binary()


# ---------------------------------------------------------------- parse_income
@settings(max_examples=500)
@given(anything)
def test_parse_income_no_crash(s):
    try:
        result = parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed on {s!r} with: {type(e).__name__}: {e}"
    # Property: result is either None (rejected) or a non-negative integer
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.integers(min_value=0, max_value=10**12))
def test_parse_income_valid_roundtrip(n):
    # Property: a properly formatted number with commas parses back to itself
    assert parse_income(f"{n:,}") == n


@given(st.from_regex(r"\A-?[0-9,]{0,8}[ .a-z]?\Z"))
def test_parse_income_near_valid(s):
    try:
        result = parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or result >= 0


# ----------------------------------------------------------------- monthly_emi
@settings(max_examples=500)
@given(anything)
def test_monthly_emi_no_crash(s):
    try:
        result = monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, float) and result > 0)


# Comma-separated triples of numbers (incl. 0, negatives, huge values)
emi_triples = st.tuples(
    st.integers(min_value=-10, max_value=10**400),
    st.integers(min_value=-10, max_value=200),
    st.integers(min_value=-10, max_value=10**6),
).map(lambda t: f"{t[0]},{t[1]},{t[2]}")


@settings(max_examples=500)
@given(emi_triples)
def test_monthly_emi_numeric_edge_cases(s):
    try:
        result = monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or result > 0


@given(
    st.integers(min_value=1000, max_value=10**8),
    st.integers(min_value=1, max_value=30),
    st.integers(min_value=1, max_value=30),
)
def test_monthly_emi_valid_property(p, rate, years):
    # Property: EMI * months must cover at least the principal (interest >= 0)
    emi = monthly_emi(f"{p},{rate},{years}")
    assert emi is not None and emi > 0
    assert emi * years * 12 >= p - 1  # allow for rounding


# ---------------------------------------------------------------- pan_category
@settings(max_examples=500)
@given(anything)
def test_pan_category_no_crash(s):
    try:
        result = pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or result in CATEGORIES.values()


@given(st.from_regex(r"\A[A-Za-z0-9]{3,11}\Z"))
def test_pan_category_near_valid(s):
    try:
        result = pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or result in CATEGORIES.values()


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=3, max_size=3),
    st.sampled_from(sorted(CATEGORIES)),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
    st.text(alphabet="0123456789", min_size=4, max_size=4),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
)
def test_pan_category_valid_property(a, cat, e, digits, last):
    # Property: every well-formed PAN maps to the category of its 4th letter
    pan = a + cat + e + digits + last
    assert pan_category(pan) == CATEGORIES[cat]
    assert pan_category(pan.lower()) == CATEGORIES[cat]
