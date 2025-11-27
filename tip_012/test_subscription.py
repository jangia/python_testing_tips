from datetime import datetime

from freezegun import freeze_time

from subscription import Subscription, is_trial_eligible


# Basic usage: freeze time with a decorator
@freeze_time("2024-01-15")
def test_subscription_is_active():
    subscription = Subscription(
        plan="premium",
        started_at=datetime(2024, 1, 1),
        duration_days=30,
    )

    assert subscription.is_active() is True
    assert subscription.days_remaining() == 16


@freeze_time("2024-02-15")
def test_subscription_is_expired():
    subscription = Subscription(
        plan="premium",
        started_at=datetime(2024, 1, 1),
        duration_days=30,
    )

    assert subscription.is_active() is False
    assert subscription.days_remaining() == 0


# Using freeze_time as a context manager
def test_trial_eligibility_with_context_manager():
    registered_at = datetime(2024, 3, 1)

    with freeze_time("2024-03-05"):
        assert is_trial_eligible(registered_at) is True

    with freeze_time("2024-03-15"):
        assert is_trial_eligible(registered_at) is False


# Moving time forward during a test
def test_subscription_expiration_over_time():
    with freeze_time("2024-01-01") as frozen_time:
        subscription = Subscription(
            plan="basic",
            started_at=datetime(2024, 1, 1),
            duration_days=7,
        )

        assert subscription.is_active() is True
        assert subscription.days_remaining() == 7

        frozen_time.move_to("2024-01-05")
        assert subscription.is_active() is True
        assert subscription.days_remaining() == 3

        frozen_time.move_to("2024-01-10")
        assert subscription.is_active() is False


# Different ways to specify the frozen time
@freeze_time("2024-06-15 14:30:00")
def test_freeze_with_specific_time():
    now = datetime.now()
    assert now.hour == 14
    assert now.minute == 30


@freeze_time(datetime(2024, 12, 25, 10, 0, 0))
def test_freeze_with_datetime_object():
    now = datetime.now()
    assert now.month == 12
    assert now.day == 25


# Tick parameter: time moves forward automatically
@freeze_time("2024-01-01 12:00:00", tick=True)
def test_with_tick_enabled():
    time_1 = datetime.now()
    # Do some work...
    time_2 = datetime.now()

    # With tick=True, time actually progresses (though very slightly)
    assert time_2 >= time_1
