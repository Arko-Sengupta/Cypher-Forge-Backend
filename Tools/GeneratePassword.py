from __future__ import annotations
import string
import secrets
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

def CalculateStrength(length: int, char_types: int) -> str:
    try:
        score = 0
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        score += char_types
        if score <= 2:
            return "Weak"
        if score <= 4:
            return "Fair"
        if score <= 6:
            return "Strong"
        return "Very Strong"
    except Exception as e:
        logger.error("Error Calculating Password Strength: %s", e, exc_info=True)
        raise e

def ShufflePassword(password_list: list[str]) -> list[str]:
    try:
        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]
        return password_list
    except Exception as e:
        logger.error("Error Shuffling Password: %s", e, exc_info=True)
        raise e

def GeneratePassword(
    length: int = 16,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_special: bool = True,
) -> dict:
    try:
        char_pools: list[str] = []
        required: list[str] = []

        if include_uppercase:
            char_pools.append(string.ascii_uppercase)
            required.append(secrets.choice(string.ascii_uppercase))
        if include_lowercase:
            char_pools.append(string.ascii_lowercase)
            required.append(secrets.choice(string.ascii_lowercase))
        if include_digits:
            char_pools.append(string.digits)
            required.append(secrets.choice(string.digits))
        if include_special:
            char_pools.append(SPECIAL_CHARACTERS)
            required.append(secrets.choice(SPECIAL_CHARACTERS))

        if not char_pools:
            raise ValueError("At least one character type must be selected.")

        all_chars = "".join(char_pools)
        remaining = [secrets.choice(all_chars) for _ in range(length - len(required))]

        password_list = ShufflePassword(required + remaining)
        password = "".join(password_list)
        strength = CalculateStrength(length, len(char_pools))

        logger.info("Password Generated Successfully (Length=%d, Strength=%s)", length, strength)

        return {
            "password": password,
            "length": length,
            "strength": strength,
        }
    except ValueError:
        raise
    except Exception as e:
        logger.error("Error Generating Password: %s", e, exc_info=True)
        raise e