from dataclasses import dataclass
from datetime import datetime, timedelta

from freezegun import freeze_time


@dataclass
class Subscription:
    plan: str
    started_at: datetime
    duration_days: int

    @property
    def expires_at(self) -> datetime:
        return self.started_at + timedelta(days=self.duration_days)

    def is_active(self) -> bool:
        return datetime.now() < self.expires_at

    def days_remaining(self) -> int:
        if not self.is_active():
            return 0
        return (self.expires_at - datetime.now()).days


# 1. Basic usage: freeze time with a decorator
@freeze_time("2024-01-15")
def test_subscription_is_active():
    subscription = Subscription(plan="premium", started_at=datetime(2024, 1, 1), duration_days=30)
    assert subscription.is_active() is True
    assert subscription.days_remaining() == 16


# 2. Context manager for testing multiple time points
def test_trial_eligibility():
    registered_at = datetime(2024, 3, 1)

    with freeze_time("2024-03-05"):
        days_since = (datetime.now() - registered_at).days
        assert days_since <= 7  # eligible

    with freeze_time("2024-03-15"):
        days_since = (datetime.now() - registered_at).days
        assert days_since > 7  # not eligible


# 3. Moving through time within a single test
def test_subscription_lifecycle():
    with freeze_time("2024-01-01") as frozen_time:
        subscription = Subscription(plan="basic", started_at=datetime(2024, 1, 1), duration_days=7)

        assert subscription.is_active() is True
        assert subscription.days_remaining() == 7

        frozen_time.move_to("2024-01-05")
        assert subscription.days_remaining() == 3

        frozen_time.move_to("2024-01-10")
        assert subscription.is_active() is False


# 4. Freeze with specific time (useful for time-of-day logic)
@freeze_time("2024-06-15 14:30:00")
def test_specific_time():
    assert datetime.now().hour == 14
    assert datetime.now().minute == 30


# 5. Allow time to tick forward (useful for timeout tests)
@freeze_time("2024-01-01 12:00:00", tick=True)
def test_time_ticks_forward():
    time_1 = datetime.now()
    time_2 = datetime.now()
    assert time_2 >= time_1
