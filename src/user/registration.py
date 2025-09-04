import re


def validate_user_info(
    flat_number: str,
    password: str,
    email: str,
) -> tuple[bool, str]:
    # Validate flat number: must be alphanumeric like "12B", "A1", etc.
    if not re.fullmatch(r"[A-Za-z0-9]+", flat_number):
        return False, "Flat number must be alphanumeric with no special characters or spaces."

    # Validate password: minimum 8 characters, at least one number and one letter
    if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return (
            False,
            "Password must be at least 8 characters long and contain both letters and numbers.",
        )

    return True, ""


def clean_flat_number(flat_number: str) -> str:
    """
    Cleans a flat number string into the format "<number><uppercase_letter>",
    where number is < 99 and letter is A-Z.

    Examples:
        "12b"   -> "12B"
        "b12"   -> "12B"
        "B-12"  -> "12B"
        "01-A"  -> "1A"
        "  7 c" -> "7C"

    Raises:
        ValueError: if input is not a valid flat number.
    """
    if not isinstance(flat_number, str):
        raise ValueError("Flat number must be a string")

    # remove spaces, hyphens, etc.
    flat_number = flat_number.strip().replace("-", "").replace(" ", "")

    # match either number-first (12B) or letter-first (B12)
    match = re.fullmatch(r"(?:(\d{1,2})([A-Za-z])|([A-Za-z])(\d{1,2}))", flat_number)
    if not match:
        raise ValueError(f"Invalid flat number format: {flat_number}")

    # extract number and letter
    if match.group(1):  # number first
        number = int(match.group(1))
        letter = match.group(2).upper()
    else:  # letter first
        number = int(match.group(4))
        letter = match.group(3).upper()

    # check constraints
    if not (1 <= number < 99):
        raise ValueError(f"Flat number must be between 1 and 98, got {number}")

    return f"{number}{letter}"
