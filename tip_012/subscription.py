from dataclasses import dataclass
from datetime import datetime, timedelta


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
        delta = self.expires_at - datetime.now()
        return delta.days


def is_trial_eligible(registered_at: datetime) -> bool:
    """Users are eligible for trial if they registered within the last 7 days."""
    days_since_registration = (datetime.now() - registered_at).days
    return days_since_registration <= 7
