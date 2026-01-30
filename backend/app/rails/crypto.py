import httpx
from decimal import Decimal

TRONGRID_URL = "https://api.trongrid.io"
USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"


class TronClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=TRONGRID_URL, timeout=10)

    async def get_trc20_balance(self, address: str) -> Decimal:
        url = f"/v1/accounts/{address}/tokens"
        resp = await self.client.get(url)
        data = resp.json()

        for token in data.get("data", []):
            if token["tokenId"] == USDT_CONTRACT:
                return Decimal(token["balance"])

        return Decimal("0")

    async def verify_transaction(self, tx_hash: str) -> bool:
        url = f"/v1/transactions/{tx_hash}"
        resp = await self.client.get(url)
        data = resp.json()

        if not data.get("data"):
            return False

        tx = data["data"][0]
        return tx.get("ret", [{}])[0].get("contractRet") == "SUCCESS"
