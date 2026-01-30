import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.models import Account, LedgerEntry, Currency


# -------- Accounts --------

async def get_or_create_account(
    db: AsyncSession,
    user_id: uuid.UUID,
    currency: Currency
) -> Account:

    result = await db.execute(
        select(Account).where(
            Account.user_id == user_id,
            Account.currency == currency
        )
    )

    account = result.scalar_one_or_none()

    if account:
        return account

    account = Account(
        user_id=user_id,
        currency=currency
    )

    db.add(account)
    await db.commit()
    await db.refresh(account)

    return account


# -------- Ledger Entries --------

async def post_entry(
    db: AsyncSession,
    account_id: uuid.UUID,
    amount: Decimal,
    reference: str
) -> LedgerEntry:

    entry = LedgerEntry(
        account_id=account_id,
        amount=amount,
        reference=reference
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry


# -------- Balance (derived) --------

async def get_balance(
    db: AsyncSession,
    account_id: uuid.UUID
) -> Decimal:

    result = await db.execute(
        select(LedgerEntry.amount).where(
            LedgerEntry.account_id == account_id
        )
    )

    amounts = result.scalars().all()
    return sum(amounts, Decimal("0.00"))
