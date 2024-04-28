from typing import Any, Union
from static.shared_types import QuestionDetails, UserDetails
import datetime

SPACE = ' '
EMPTY = ''

def check_for_whitespace(items: Union[dict, UserDetails, QuestionDetails]) -> bool:
    for key, value in items.items():
        if not isinstance(value, str): continue
        elif 'option' in key: continue
        if SPACE in value: print(f'{key}: {value} has whitespace in it'); return True
    return False


def check_for_empty(items: Union[dict, UserDetails, QuestionDetails]) -> bool:
    for _, value in items.items():
        if not isinstance(value, str):
            continue
        if value == EMPTY:
            return True
    return False


def validate_date(date_string: str) -> bool:
    try:
        datetime.date.fromisoformat(date_string)
        return True
    except ValueError:
        return False
    

def check_for_duplicates(items: list, exception: Any = None) -> bool:
    seen = []
    for item in items:
        if item == exception: continue
        elif item in seen: return True
        else: seen.append(item)
    return False