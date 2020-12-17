from typing import Optional, Callable
import os

from tqdm import tqdm


def __call__(main: Callable[[str], None], file_path: Optional[str], directory_path: Optional[str]):
    if all([file_path, directory_path]):
        raise AttributeError('Pass either file path or directory path')

    if directory_path:
        progress_bar = tqdm(os.listdir(directory_path))
        for file in progress_bar:
            progress_bar.set_description(f'Processing {file}', refresh=True)
            main(image_file_path=os.path.join(directory_path, file))
    else:
        main(image_file_path=file_path)
