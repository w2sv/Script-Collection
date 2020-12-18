import os
from typing import Tuple, List, Optional

import numpy as np
from tqdm import tqdm

from src.utils import kick_off_message_displayer


class IndexedPixel(np.ndarray):
    """ Serving the convenient storage of the pixel location indices """

    def __new__(cls, rgb_values: np.ndarray, indices: Tuple[int, int]):
        """ Args:
        rgb_values: ndarray of shape (3, )
        indices: Tuple[row, column] """

        obj = rgb_values.view(cls)
        obj.indices = indices
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        self.indices = getattr(obj, 'indices', None)


@kick_off_message_displayer('Sequentializing pixels...')
def get_indexed_pixels(image: np.ndarray) -> List[IndexedPixel]:
    indexed_pixels = []

    for i, row in enumerate(image):
        for j, pixel in enumerate(row):
            indexed_pixels.append(IndexedPixel(pixel, indices=(i, j)))

    return indexed_pixels


@kick_off_message_displayer('Restoring image...')
def restore_image(pixel_clusters: List[IndexedPixel], image_shape: Tuple[int]) -> np.ndarray:
    """ Assign image of equal shape as the original one with the means of
        the rgb value clusters the respective pixels ended up in """

    image = np.zeros(shape=image_shape)

    for pixel_cluster in tqdm(pixel_clusters):
        cluster_mean = np.mean(pixel_cluster, axis=0)

        for pixel in pixel_cluster:
            image[pixel.indices] = cluster_mean

    return image


def get_write_path(original_path: str, write_dir_path: Optional[str], n_clusters: int, conducted_iterations: int) -> str:
    """ Returns:
            altered image file name being extended by n_clusters and conducted_iterations,
            prepended either by dir path original image residing in if write dir path not
            set, or write dir path otherwise """

    extension_stripped_path, extension = os.path.splitext(original_path)
    suffix = f'_{n_clusters}clusters_{conducted_iterations}iterations' + extension

    if write_dir_path is None:
        return extension_stripped_path + suffix

    file_name = original_path.split(os.sep)[-1]
    return os.path.join(write_dir_path, file_name + suffix)
