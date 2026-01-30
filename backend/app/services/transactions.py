from decimal import Decimal
from .ledger import Ledger
from .risk import RiskEngine
from .idempotency import IdempotencyStore


class TransactionEngine:
    def __init__(self, ledger: Ledger, risk: RiskEngine, idem: IdempotencyStore):
        self.ledger = ledger
        self.risk = risk
        self.idem = idem

    def execute(self, idempotency_key: str, user_id: str, amount: Decimal, direction: str):
        if self.idem.exists(idempotency_key):
            return self.idem.get(idempotency_key)

        self.risk.check_transaction(amount)

        if direction == "DEBIT":
            self.ledger.debit(user_id, amount)
        elif direction == "CREDIT":
            self.ledger.credit(user_id, amount)
        else:
            raise Exception("INVALID_DIRECTION")

        result = {"status": "OK"}
        self.idem.set(idempotency_key, result)
        return result
