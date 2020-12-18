import os
from typing import Tuple, Type, Optional, Any, Callable
import argparse
import functools

from tqdm import tqdm


def parse_args(*arguments: Tuple[str, str, Type, str, Optional[Any]], include_dir_argument=False):
    """ Arguments arguments, listed chronologically:
            shorthand cli invocation keyword
            cli invocation keyword
            option type
            help description
            default value """

    parser = argparse.ArgumentParser()

    if include_dir_argument:
        arguments += (('-d', '--dir', str, 'directory path', None), )

    for arg in arguments:
        parser.add_argument(*arg[:2], type=arg[2], help=arg[3], default=arg[4])

    return parser.parse_args()


def kick_off_message_displayer(message: str):
    """ Display kick off message before execution of decorated function """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def run(main: Callable[[str], None], file_path: Optional[str], directory_path: Optional[str]):
    """ Runs main either over all files within passed dir in case of dir path
        reception or over passed file path respectively

        Args:
            main: execution function, to receive merely an absolute file path argument and
                not to return anything
            file_path: leading to file main shall be run against
            directory_path: comprising files all of which main shall be run against

        Raises:
            AttributeError on either the absence of either file_path or directory_path or
                the passing of both """

    if all([file_path, directory_path]) or not any([file_path, directory_path]):
        raise AttributeError('Pass either file path or directory path')

    if directory_path:
        progress_bar = tqdm(os.listdir(directory_path))
        for file in progress_bar:
            progress_bar.set_description(f'Processing {file}', refresh=True)
            main(os.path.join(directory_path, file))
    else:
        main(file_path)
