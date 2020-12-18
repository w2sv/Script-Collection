""" Identifies all duplicates of files whose types ought to be considered
    residing with any depth under passed root directory by file name and
    disk usage, and moves them on identification to trash for a possible
    manual duplicate status verification and consecutive irreversible removal

    Args:
        --root: root directory path which shall be scoured for and stripped of file duplicates
        --fileextensions: extensions whose corresponding files ought to be searched for duplicates
            on encounter, to be passed as comma-separated string """

from src.file_duplicate_remover import get_reference_file


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
