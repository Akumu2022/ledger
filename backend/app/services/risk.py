from decimal import Decimal

MAX_SINGLE_TX = Decimal("2000")


def risk_check(amount: Decimal):
    if amount > MAX_SINGLE_TX:
        raise Exception("TX_LIMIT_EXCEEDED")
    return True
