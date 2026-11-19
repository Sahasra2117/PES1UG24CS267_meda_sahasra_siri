"""Lab 6 - Code (line/statement) coverage tests for hotel_booking.py.

Goal: execute every statement in hotel_booking.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_hotel_booking_application.py
    coverage report -m
"""
import pytest

from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---------------------------------------------------------------- booking_cost
def test_standard_two_nights():
    # starter example: off-peak, 2 guests, short stay
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 2, 2, False)


def test_invalid_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_peak_extra_guests_long_stay():
    # peak: 2000 + 500 = 2500/night * 7 = 17500
    # 1 extra guest: 500 * 7 = 3500 -> 21000
    # 7+ nights: 10% off -> 21000 - 2100 = 18900
    assert booking_cost("standard", 7, 3, True) == 18900


# --------------------------------------------------------- cancellation_refund
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund_member_bonus():
    # 2-6 days before: 50% + member bonus 25%
    assert cancellation_refund(1000, 3, True) == 750


def test_no_refund_last_minute():
    assert cancellation_refund(1000, 1, False) == 0


# ---------------------------------------------------------------- room_upgrade
def test_no_upgrade_when_no_rooms_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_member_standard_upgraded_to_deluxe():
    assert room_upgrade("standard", True, 2) == "deluxe"


def test_member_deluxe_upgraded_to_suite():
    assert room_upgrade("deluxe", True, 2) == "suite"


def test_suite_not_upgraded():
    assert room_upgrade("suite", True, 2) == "suite"
