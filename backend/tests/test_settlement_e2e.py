import pytest
from decimal import Decimal

from app.services.ledger import Ledger
from app.services.treasury import Treasury
from app.services.reconciliation import Reconciliation
from app.services.settlement import SettlementEngine
from app.services.risk import risk_check


class MockSigner:
    async def sign_and_broadcast(self, tx_payload: dict) -> str:
        return "MOCK_TX_HASH"


@pytest.mark.asyncio
async def test_settlement_flow():
    # Core components
    ledger = Ledger()
    treasury = Treasury(signer=MockSigner())
    recon = Reconciliation()

    engine = SettlementEngine(
        ledger=ledger,
        treasury=treasury,
        risk_check=risk_check,
        reconciliation=recon
    )

    # Seed user balance
    ledger.credit("user1", Decimal("500"))

    # Execute withdrawal
    result = await engine.process_withdrawal(
        tx_id="tx_001",
        user_id="user1",
        amount=Decimal("100"),
        to_address="TTestAddress123"
    )

    # Assertions
    assert result["status"] == "SETTLED"
    assert result["tx_hash"] == "MOCK_TX_HASH"
    assert ledger.get_balance("user1") == Decimal("400")
