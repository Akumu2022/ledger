from decimal import Decimal
from app.services.transactions import Transaction


class SettlementEngine:
    def __init__(self, ledger, treasury, risk_check, reconciliation):
        self.ledger = ledger
        self.treasury = treasury
        self.risk_check = risk_check
        self.reconciliation = reconciliation

    async def process_withdrawal(
        self,
        tx_id: str,
        user_id: str,
        amount: Decimal,
        to_address: str
    ):
        self.risk_check(amount)

        tx = Transaction(tx_id, user_id, amount)

        self.ledger.debit(user_id, amount)

        tx_hash = await self.treasury.withdraw_usdt(
            to_address=to_address,
            amount=amount
        )

        tx.settle()

        return {
            "tx_id": tx.tx_id,
            "status": tx.status,
            "tx_hash": tx_hash
        }
