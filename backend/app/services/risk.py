from datetime import datetime, timedelta
from decimal import Decimal

SYSTEM_STATUS = "ACTIVE"

# ---- Kill Switch ----

def freeze_system():
    global SYSTEM_STATUS
    SYSTEM_STATUS = "FROZEN"

def unfreeze_system():
    global SYSTEM_STATUS
    SYSTEM_STATUS = "ACTIVE"

def assert_system_active():
    if SYSTEM_STATUS != "ACTIVE":
        raise Exception("SYSTEM IS FROZEN")


# ---- User Tiers ----

USER_TIERS = {
    "TIER_1": Decimal("500"),
    "TIER_2": Decimal("1500"),
    "TIER_3": Decimal("10000"),
}

# ---- Velocity Rules ----

VELOCITY_RULES = {
    "TIER_1": {"count": 5, "window_minutes": 60},
    "TIER_2": {"count": 20, "window_minutes": 60},
    "TIER_3": {"count": 100, "window_minutes": 60},
}

# ---- Risk Checks ----

def check_user_limit(tier: str, amount: Decimal):
    if amount > USER_TIERS[tier]:
        raise Exception("User limit exceeded")

def check_velocity(recent_tx_count: int, tier: str):
    if recent_tx_count >= VELOCITY_RULES[tier]["count"]:
        raise Exception("Velocity limit exceeded")

def check_cooling_period(
    user_created_at: datetime,
    required_hours: int = 24
):
    if datetime.utcnow() - user_created_at < timedelta(hours=required_hours):
        raise Exception("User in cooling period")

def risk_check(
    tier: str,
    amount: Decimal,
    recent_tx_count: int,
    user_created_at: datetime
):
    assert_system_active()
    check_user_limit(tier, amount)
    check_velocity(recent_tx_count, tier)
    check_cooling_period(user_created_at)
