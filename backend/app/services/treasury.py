from decimal import Decimal
from datetime import datetime
from .signer import EnvSigner

USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

KILL_SWITCH = False
DAILY_WITHDRAW_LIMIT = Decimal("5000")


class Treasury:
    def __init__(self, signer=None):
        self.signer = signer or EnvSigner()
        self.daily_withdrawn = Decimal("0")
        self.last_reset = datetime.utcnow().date()

    def _reset_if_new_day(self):
        today = datetime.utcnow().date()
        if today != self.last_reset:
            self.daily_withdrawn = Decimal("0")
            self.last_reset = today

    def authorize(self, amount: Decimal):
        if KILL_SWITCH:
            raise Exception("SYSTEM_HALTED")

        self._reset_if_new_day()

        if self.daily_withdrawn + amount > DAILY_WITHDRAW_LIMIT:
            raise Exception("DAILY_LIMIT_REACHED")

        self.daily_withdrawn += amount

    async def withdraw_usdt(self, to_address: str, amount: Decimal):
        self.authorize(amount)

        tx_payload = {
            "to": to_address,
            "amount": amount,
            "contract": USDT_CONTRACT
        }

        tx_hash = await self.signer.sign_and_broadcast(tx_payload)
        return tx_hash
