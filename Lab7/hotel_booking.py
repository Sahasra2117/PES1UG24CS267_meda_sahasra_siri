"""Hotel booking helpers - hardened against invalid input (Lab 7 fix).

Every function returns None instead of crashing when the input is invalid.
"""


def _parse_ascii_int(text):
    """Return int(text) if text is a non-empty run of ASCII digits, else None."""
    text = text.strip()
    if not text or not text.isascii() or not text.isdigit():
        return None
    return int(text)


def nights_stayed(days):
    """'12-15' -> 3. Returns None for malformed input or check-out before check-in."""
    if not isinstance(days, str):
        return None
    parts = days.split('-')
    if len(parts) != 2:
        return None
    check_in = _parse_ascii_int(parts[0])
    check_out = _parse_ascii_int(parts[1])
    if check_in is None or check_out is None:
        return None
    if not 1 <= check_in <= 31 or not 1 <= check_out <= 31:
        return None
    if check_out < check_in:
        return None
    return check_out - check_in


def room_floor(room_code):
    """'D-305' -> 3. Returns None if the code is not <letters>-<digits>."""
    if not isinstance(room_code, str):
        return None
    parts = room_code.strip().split('-')
    if len(parts) != 2:
        return None
    block, number = parts[0].strip(), parts[1].strip()
    if not block or not block.isascii() or not block.isalpha():
        return None
    if _parse_ascii_int(number) is None:
        return None
    return int(number[0])


def booking_label(names_csv):
    """'ravi, priya' -> 'Ravi +1'. Returns None if there is no guest name."""
    if not isinstance(names_csv, str):
        return None
    names = [n.strip() for n in names_csv.split(',') if n.strip()]
    if not names:
        return None
    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


def _ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""


def main():
    print("==== Running nights_stayed ====")
    result = nights_stayed(_ask("Enter check-in and check-out day (e.g. 12-15): "))
    print("Nights:", result if result is not None else "Invalid input")

    print("\n==== Running room_floor ====")
    result = room_floor(_ask("Enter a room code (e.g. D-305): "))
    print("Floor:", result if result is not None else "Invalid input")

    print("\n==== Running booking_label ====")
    result = booking_label(_ask("Enter guest names as CSV (e.g. ravi, priya): "))
    print("Booking Label:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
