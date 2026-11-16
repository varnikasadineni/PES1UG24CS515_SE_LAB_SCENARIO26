import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

# Sensible upper limits so huge inputs can't overflow or hang the program
MAX_AMOUNT = 10**12        # 1 lakh crore
MAX_RATE = 100             # % per annum
MAX_YEARS = 50

AMOUNT_RE = re.compile(r"[0-9]{1,3}(,[0-9]{2,3})*|[0-9]+", re.ASCII)
RATE_RE = re.compile(r"[0-9]+(\.[0-9]+)?", re.ASCII)
YEARS_RE = re.compile(r"[0-9]+", re.ASCII)
PAN_RE = re.compile(r"[A-Z]{3}[A-Z][A-Z][0-9]{4}[A-Z]", re.ASCII)


def parse_income(income):
    """Parse an income like '50,000' or '5,00,000'. Returns int, or None if invalid."""
    if not isinstance(income, str):
        return None
    income = income.strip()
    if len(income) > 20 or not AMOUNT_RE.fullmatch(income):
        return None
    value = int(income.replace(",", ""))
    if value > MAX_AMOUNT:
        return None
    return value


def monthly_emi(details):
    """Compute EMI from 'principal,rate,years'. Returns float, or None if invalid."""
    if not isinstance(details, str) or len(details) > 50:
        return None
    parts = [p.strip() for p in details.split(",")]
    if len(parts) != 3:
        return None
    principal_s, rate_s, years_s = parts
    if not (YEARS_RE.fullmatch(principal_s) and RATE_RE.fullmatch(rate_s)
            and YEARS_RE.fullmatch(years_s)):
        return None

    principal = int(principal_s)
    rate = float(rate_s)
    years = int(years_s)
    if not (0 < principal <= MAX_AMOUNT and 0 <= rate <= MAX_RATE and 0 < years <= MAX_YEARS):
        return None

    n = years * 12
    if rate == 0:                       # 0% loan: avoid division by zero
        return round(principal / n, 2)
    r = rate / 1200
    factor = (1 + r) ** n
    return round(principal * r * factor / (factor - 1), 2)


def pan_category(pan):
    """Return the holder category of a PAN like 'ABCPE1234F', or None if invalid/unknown."""
    if not isinstance(pan, str):
        return None
    pan = pan.strip()
    if len(pan) != 10 or not pan.isascii():
        return None
    pan = pan.upper()
    if not PAN_RE.fullmatch(pan):
        return None
    return CATEGORIES.get(pan[3])


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result if result is not None else "Invalid income")

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result if result is not None else "Invalid loan details")

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()
