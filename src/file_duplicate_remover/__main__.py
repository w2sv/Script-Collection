""" Identifies all duplicates of files whose types ought to be considered
    residing with any depth under passed root directory by file name and
    disk usage, and moves them on identification to trash for a possible
    manual duplicate status verification and consecutive irreversible removal

    Args:
        --root: root directory path which shall be scoured for and stripped of file duplicates
        --fileextensions: extensions whose corresponding files ought to be searched for duplicates
            on encounter, to be passed as comma-separated string """
import os
from pathlib import Path
from typing import Iterator

from send2trash import send2trash
from tqdm import tqdm


def get_reference_file(dir_path: str) -> Iterator[int]:
    """ Walks through all file system objects residing in dir_path,
        either triggers duplicates search and removal if encountering file which
        ought to be considered, or recurses on encounter of non-empty directory
        respectively

        Args:
            dir_path: directory path to be walked through and triggered duplicate search
                from, := recursion parameter

        Yields:
            disk usage of removed duplicates in byte """

    p_bar = tqdm(os.listdir(dir_path))
    for file in p_bar:
        file_path = os.path.join(dir_path, file)

        # recurse if happening upon dir
        if os.path.isdir(file_path):
            if dir_path == ROOT_DIR_PATH:
                p_bar.set_description(f'Walking through {file}...')
            get_reference_file(file_path)

        # search for duplicates and remove if existent
        elif _consider_file(file_path):
            yield from _remove_duplicates(file_path, dir_path=ROOT_DIR_PATH)


def _consider_file(file_path: str) -> bool:
    return _file_extension(file_path) in FILE_EXTENSIONS_2_CONSIDER


def _file_extension(file_path: str) -> str:
    """ Returns:
            file extension without dot, e.g. 'mp3', 'wav' etc.

        >>> _file_extension("C:\\Users\\User\\Music\\Flume\\B.I.G Flume (Album Mix) - YouTube.mp3")
        'mp3' """

    return os.path.splitext(file_path)[1][1:]


def _remove_duplicates(reference_file_path: str, dir_path: str) -> Iterator[int]:
    """ Walks through all file system objects residing in dir_path,
        either checks whether duplicate of file residing under reference_file_path
        and if so moves to trash if encountering file, or recurses on
        encounter of non-empty directory respectively

        Args:
            reference_file_path: path of file whose duplicates shall be removed
            dir_path: path under which to search for duplicate, := recursion
                parameters

        Yields:
            disk usage of removed duplicates in byte"""

    for candidate in os.listdir(dir_path):
        candidate_file_path = os.path.join(dir_path, candidate)

        # recurse on encounter of non-empty directory
        if os.path.isdir(candidate_file_path) and os.listdir(candidate_file_path):
            yield from _remove_duplicates(reference_file_path, dir_path=candidate_file_path)

        # move candidate to trash if containing_dir != containing_dir_reference_file,
        # file worthy of being considered given its extension and contained file
        # and reference file identical
        elif dir_path != str(Path(reference_file_path).parent) and _consider_file(candidate_file_path) and _contain_identical_file(reference_file_path, candidate_file_path):
            yield os.path.getsize(candidate_file_path)

            send2trash(candidate_file_path)
            print(f"Removed {_relative_path(reference_file_path)} duplicate residing at {dir_path}")

            # move directory to trash if empty
            if not os.listdir(dir_path):
                send2trash(dir_path)


def _contain_identical_file(*paths: str) -> bool:
    """ Judges by whether or not files residing under paths possess
        identical file name with extension and are of identical size """

    return len(set(map(lambda path: (_file_name_with_extension(path), os.path.getsize(path)), paths))) == 1


def _file_name_with_extension(file_path: str) -> str:
    """
    >>> _file_name_with_extension("C:\\Users\\User\\Music\\Flume\\B.I.G Flume (Album Mix) - YouTube.mp3")
    'B.I.G Flume (Album Mix) - YouTube.mp3' """

    return file_path.split(os.sep)[-1]


def _relative_path(absolute_path: str) -> str:
    """ Returns:
            relative path with respect to ROOT_DIR_PATH """

    return absolute_path[len(ROOT_DIR_PATH):]


if __name__ == '__main__':
    from src.utils import parse_args

    # parse args
    args = parse_args(
        ('-r', '--rootdir', str, 'root directory whose comprised file duplicates shall be removed', None),
        ('-f', '--fileextensions', str, 'extentions of files who shall be considered', 'wma, MP3, mp3, m4a, wav')
    )
    
    ROOT_DIR_PATH = args.rootdir
    FILE_EXTENSIONS_2_CONSIDER = set(args.fileextensions.replace(' ', '').split(','))

    # remove duplicates
    removed_file_sizes = list(get_reference_file(dir_path=ROOT_DIR_PATH))
    
    # display number and total disk usage of removed duplicates
    print(f'Removed {len(removed_file_sizes)} duplicates of a total of {sum(removed_file_sizes) / 1e6:.2f}MB')
