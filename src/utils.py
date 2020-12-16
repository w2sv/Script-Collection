from typing import Tuple, Type
import argparse


def parse_args(*arguments: Tuple[str, str, Type, str]):    
    parser = argparse.ArgumentParser()

    for arg in arguments:
        parser.add_argument(*arg[:2], type=arg[2], help=arg[3])

    return parser.parse_args()
