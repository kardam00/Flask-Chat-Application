from string import ascii_letters
import random
from typing import List


def generate_room_code(length: int, existing_codes: List[str]) -> str:
    while True:
        code_chars = [random.choice(ascii_letters) for _ in range(length)]
        code = ''.join(code_chars)

        if code not in existing_codes:
            return code
