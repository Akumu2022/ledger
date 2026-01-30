from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import Transaction, TransactionStatus

RECONCILIATION_THRESHOLD_MINUTES = 30


async def find_stale_transactions(db: AsyncSession):
    cutoff = datetime.utcnow() - timedelta(
        minutes=RECONCILIATION_THRESHOLD_MINUTES
    )

    result = await db.execute(
        """
        SELECT * FROM transactions
        WHERE status = 'PENDING'
        AND created_at < :cutoff
        """,
        {"cutoff": cutoff}
    )

    return result.fetchall()


async def mark_transaction_failed(
    db: AsyncSession,
    tx_id
):
    tx = await db.get(Transaction, tx_id)
    if not tx:
        return

    tx.status = TransactionStatus.FAILED
    await db.commit()


async def reconcile_external_payment(
    db: AsyncSession,
    tx_id,
    external_amount,
    external_reference
):
    tx = await db.get(Transaction, tx_id)

    if not tx:
        raise Exception("Transaction not found")

    if tx.amount != external_amount:
        raise Exception("Amount mismatch")

    if tx.external_ref != external_reference:
        raise Exception("Reference mismatch")

    return True


async def reconciliation_job(db: AsyncSession):
    stale = await find_stale_transactions(db)

    for tx in stale:
        await mark_transaction_failed(db, tx.id)
