import uuid
from sqlalchemy import (
    Column, String, DateTime, Numeric, ForeignKey, Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# ---- Enums ----

class Currency(str, enum.Enum):
    USD = "USD"
    KES = "KES"
    USDT = "USDT"

class TransactionStatus(str, enum.Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# ---- Core Tables ----

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    currency = Column(Enum(Currency), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ledger_entries = relationship("LedgerEntry", back_populates="account")


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    amount = Column(Numeric(18, 2), nullable=False)  # + credit, - debit
    reference = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="ledger_entries")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_ref = Column(String, unique=True, nullable=False)
    from_currency = Column(Enum(Currency), nullable=False)
    to_currency = Column(Enum(Currency), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.CREATED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
