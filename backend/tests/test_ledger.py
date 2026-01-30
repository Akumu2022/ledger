from decimal import Decimal
from app.services.ledger import Ledger


def test_ledger_credit_debit():
    ledger = Ledger()

    ledger.credit("user1", Decimal("100"))
    assert ledger.get_balance("user1") == Decimal("100")

    ledger.debit("user1", Decimal("40"))
    assert ledger.get_balance("user1") == Decimal("60")
