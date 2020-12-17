from typing import Tuple, Type, Optional, Any
import argparse
import functools


def parse_args(*arguments: Tuple[str, str, Type, str, Optional[Any]]):
    parser = argparse.ArgumentParser()

    for arg in arguments:
        parser.add_argument(*arg[:2], type=arg[2], help=arg[3], default=arg[4])

    return parser.parse_args()


def kick_off_message_displayer(message: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
