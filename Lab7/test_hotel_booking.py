"""Lab 7 - Property-based fuzz tests for hotel_booking.py using Hypothesis.

Run:  python -m pytest test_hotel_booking.py
"""
from hypothesis import given, settings, strategies as st

from hotel_booking import nights_stayed, room_floor, booking_label

settings.register_profile("lab7", max_examples=300, deadline=None)
settings.load_profile("lab7")

# Mix of totally random input and "almost valid" input so the fuzzer
# reaches the interesting edge cases (empty parts, extra dashes, etc.).
FUZZ = (
    st.text()
    | st.none()
    | st.integers()
    | st.from_regex(r"\A[0-9-]{0,8}\Z")
    | st.from_regex(r"\A[A-Za-z]{0,2}-?[0-9A-Za-z]{0,4}\Z")
    | st.from_regex(r"\A[ ,a-z]{0,12}\Z")
)


# ---------------------------------------------------------------- crash tests
@given(FUZZ)
def test_nights_stayed_no_crash(s):
    try:
        nights_stayed(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"nights_stayed({s!r}) crashed with: {type(e).__name__}: {e}"


@given(FUZZ)
def test_room_floor_no_crash(s):
    try:
        room_floor(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"room_floor({s!r}) crashed with: {type(e).__name__}: {e}"


@given(FUZZ)
def test_booking_label_no_crash(s):
    try:
        booking_label(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"booking_label({s!r}) crashed with: {type(e).__name__}: {e}"


# ------------------------------------------------------ correctness properties
@given(st.integers(1, 31), st.integers(1, 31))
def test_nights_stayed_valid_range(check_in, check_out):
    result = nights_stayed(f"{check_in}-{check_out}")
    if check_out >= check_in:
        assert result == check_out - check_in
    else:
        # check-out before check-in is not a valid stay
        assert result is None


@given(st.integers(1, 31), st.integers(1, 31))
def test_nights_stayed_never_negative(check_in, check_out):
    result = nights_stayed(f"{check_in}-{check_out}")
    assert result is None or result >= 0


@given(st.sampled_from("ABCDS"), st.integers(1, 9), st.integers(0, 99))
def test_room_floor_valid_codes(block, floor, room):
    code = f"{block}-{floor}{room:02d}"
    assert room_floor(code) == floor


@given(st.lists(st.from_regex(r"\A[a-z]{1,10}\Z"), min_size=1, max_size=6))
def test_booking_label_valid_names(names):
    label = booking_label(", ".join(names))
    lead = names[0]
    assert label == lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


@given(FUZZ)
def test_invalid_input_returns_none_or_expected_type(s):
    assert nights_stayed(s) is None or isinstance(nights_stayed(s), int)
    assert room_floor(s) is None or isinstance(room_floor(s), int)
    assert booking_label(s) is None or isinstance(booking_label(s), str)
