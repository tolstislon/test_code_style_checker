"""Constants"""

from typing import Final, Tuple

CLASS: Final[str] = 'class'
DEF: Final[str] = 'def'
MIN_LENGTH_VARIABLE: Final[int] = 4
BAD_VARIABLE_NAME: Tuple[str, ...] = ('qwer', 'qwert', 'qwerty', 'asdf', 'asdfg', 'zxcv')
GOOD_VARIABLE_NAME: Tuple[str, ...] = (
    'api', 'in', 'not', 'is', 'or', 'and', 'for', 'tag', 'i', 'max', 'min', 'int', 'set', 'str', 'all', 'any'
)
