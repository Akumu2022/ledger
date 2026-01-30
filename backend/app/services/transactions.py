import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import Transaction, TransactionStatus, Currency
from services.ledger import get_or_create_account, post_entry
from services.risk import assert_system_active


async def create_transaction(
    db: AsyncSession,
    external_ref: str,
    from_currency: Currency,
    to_currency: Currency,
    amount: Decimal
) -> Transaction:

    tx = Transaction(
        external_ref=external_ref,
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        status=TransactionStatus.CREATED
    )

    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx


async def execute_transaction(
    db: AsyncSession,
    tx_id: uuid.UUID,
    user_id: uuid.UUID,
    rate: Decimal
):

    assert_system_active()

    tx = await db.get(Transaction, tx_id)

    if not tx or tx.status != TransactionStatus.CREATED:
        raise Exception("Invalid transaction state")

    tx.status = TransactionStatus.PENDING
    await db.commit()

    try:
        from_account = await get_or_create_account(
            db, user_id, tx.from_currency
        )

        to_account = await get_or_create_account(
            db, user_id, tx.to_currency
        )

        debit_amount = -tx.amount
        credit_amount = tx.amount * rate

        await post_entry(
            db,
            from_account.id,
            debit_amount,
            reference=f"TX:{tx.id}"
        )

        await post_entry(
            db,
            to_account.id,
            credit_amount,
            reference=f"TX:{tx.id}"
        )

        tx.status = TransactionStatus.COMPLETED
        await db.commit()

    except Exception:
        tx.status = TransactionStatus.FAILED
        await db.commit()
        raise
