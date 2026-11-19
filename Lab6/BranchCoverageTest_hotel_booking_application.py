"""Lab 6 - Branch coverage tests for hotel_booking.py.

Goal: every decision (if / elif / else) evaluates to both True and False.
Run:
    coverage run --branch -m pytest BranchCoverageTest_hotel_booking_application.py
    coverage report -m
"""
import pytest

from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---------------------------------------------------------------- booking_cost
# Decisions: room in ROOM_RATE | nights < 1 | is_peak_season | guests > 2 |
#            nights >= 7
def test_unknown_room_raises():                       # room check -> True
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 2, 2, False)


@pytest.mark.parametrize("nights", [0, -3])
def test_invalid_nights_raises(nights):               # nights < 1 -> True
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("deluxe", nights, 2, False)


def test_offpeak_two_guests_short_stay():             # all optional -> False
    assert booking_cost("standard", 2, 2, False) == 4000


def test_one_night_boundary():                        # nights == 1 is valid
    assert booking_cost("suite", 1, 1, False) == 6000


def test_peak_season_only():                          # peak -> True
    # deluxe 3500 + 875 = 4375 * 3 = 13125
    assert booking_cost("deluxe", 3, 2, True) == 13125


def test_extra_guests_only():                         # guests > 2 -> True
    # 2000 * 2 = 4000 + 2 extra * 500 * 2 = 2000 -> 6000
    assert booking_cost("standard", 2, 4, False) == 6000


def test_long_stay_discount_boundary():               # nights >= 7 -> True
    # suite 6000 * 7 = 42000 - 4200 = 37800
    assert booking_cost("suite", 7, 2, False) == 37800


def test_six_nights_no_discount():                    # nights >= 7 -> False
    assert booking_cost("standard", 6, 2, False) == 12000


def test_everything_applies():
    # peak 2500 * 7 = 17500 + 500 * 7 = 3500 -> 21000 - 2100 = 18900
    assert booking_cost("standard", 7, 3, True) == 18900


# --------------------------------------------------------- cancellation_refund
# Decisions: days_before >= 7 | days_before >= 2 | is_member
@pytest.mark.parametrize("member", [True, False])
def test_full_refund_7_days_or_more(member):          # first if -> True
    assert cancellation_refund(1000, 7, member) == 1000
    assert cancellation_refund(1000, 30, member) == 1000


def test_half_refund_non_member():                    # elif True, member False
    assert cancellation_refund(1000, 2, False) == 500


def test_half_refund_member():                        # elif True, member True
    assert cancellation_refund(1000, 6, True) == 750


def test_no_refund_non_member():                      # else, member False
    assert cancellation_refund(1000, 1, False) == 0


def test_no_refund_member_gets_bonus():               # else, member True
    assert cancellation_refund(1000, 0, True) == 250


# ---------------------------------------------------------------- room_upgrade
# Decisions: rooms_free == 0 | standard & member | deluxe & member
def test_no_rooms_free():                             # rooms_free == 0 -> True
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgraded():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_standard_non_member_not_upgraded():          # both conditions False
    assert room_upgrade("standard", False, 1) == "standard"


def test_deluxe_member_upgraded():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_deluxe_non_member_not_upgraded():
    assert room_upgrade("deluxe", False, 1) == "deluxe"


def test_suite_stays_suite():
    assert room_upgrade("suite", True, 5) == "suite"
