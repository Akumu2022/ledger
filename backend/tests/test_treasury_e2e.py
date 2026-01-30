import pytest
from decimal import Decimal
from app.services.treasury import Treasury


class MockSigner:
    async def sign_and_broadcast(self, tx_payload: dict) -> str:
        return "MOCK_TX_HASH"


@pytest.mark.asyncio
async def test_treasury_withdraw():
    treasury = Treasury(signer=MockSigner())

    tx_hash = await treasury.withdraw_usdt(
        to_address="TTestAddress123",
        amount=Decimal("100")
    )

    assert tx_hash == "MOCK_TX_HASH"
