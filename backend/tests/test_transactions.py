from decimal import Decimal
from app.services.ledger import Ledger
from app.services.transactions import Transaction, TransactionEngine


def test_transaction_engine():
    ledger = Ledger()
    ledger.credit("user1", Decimal("100"))

    engine = TransactionEngine(ledger)
    tx = Transaction("tx1", "user1", Decimal("50"))

    engine.execute(tx, "DEBIT")

    assert ledger.get_balance("user1") == Decimal("50")
    assert tx.status == "SETTLED"
