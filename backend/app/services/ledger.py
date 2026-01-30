from decimal import Decimal
from collections import defaultdict


class Ledger:
    def __init__(self):
        self.balances = defaultdict(Decimal)

    def credit(self, user_id: str, amount: Decimal):
        self.balances[user_id] += amount

    def debit(self, user_id: str, amount: Decimal):
        if self.balances[user_id] < amount:
            raise Exception("INSUFFICIENT_FUNDS")
        self.balances[user_id] -= amount

    def get_balance(self, user_id: str) -> Decimal:
        return self.balances[user_id]
