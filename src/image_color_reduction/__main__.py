""" Reduce quantity of colors present in image by means of kMeans clustering the entirety
	of rgb values present in the original image and subsequently assigning the image
	pixels with the cluster means they ended up in.
	Original file will be left untouched.

	Refer to the bottom of this file in order to read up on the passable cli options. """


from typing import Tuple, List
import os

from tqdm import tqdm
import numpy as np
import cv2

from src.utils import kick_off_message_displayer
from src.image_color_reduction.k_means_clustering import KMeansClusterer


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


def get_write_path(original_path: str, n_clusters: int, conducted_iterations: int) -> str:
	""" Returns:
			altered image file name being extended by n_clusters and conducted_iterations,
			prepended either by dir path original image residing in if write dir path not
			set, or write dir path otherwise """

	extension_stripped_path, extension = os.path.splitext(original_path)
	suffix = f'_{n_clusters}clusters_{conducted_iterations}iterations' + extension

	if WRITE_DIR_PATH is None:
		return extension_stripped_path + suffix

	file_name = original_path.split(os.sep)[-1]
	return os.path.join(WRITE_DIR_PATH, file_name + suffix)


def main(image_file_path: str):
	# open image and get indexed, sequentialized pixels
	original_image = cv2.imread(image_file_path)
	indexed_pixels = get_indexed_pixels(original_image)

	# cluster rgb values being present in image
	clusterer = KMeansClusterer(indexed_pixels, N_CLUSTERS, max_iterations=MAX_ITERATIONS, seed=SEED)
	clusters = clusterer.__call__()

	# write color reduced image
	write_path = get_write_path(image_file_path, n_clusters=N_CLUSTERS, conducted_iterations=clusterer.n_conducted_iterations)
	cv2.imwrite(write_path, restore_image(clusters, image_shape=original_image.shape))
	print(f'Saved color reduced image to {write_path}')


if __name__ == '__main__':
	from src.utils import parse_args, run

	args = parse_args(
		('-p', '--path', str, 'image path', None),
		('-c', '--clusters', int, 'number of desired colors image colors will be reduced to', 10),
		('-m', '--maxiterations', int, 'maximal amount of conducted kMeans clustering iterations', 5),
		('-s', '--seed', int, 'rng seed, affects centroid initialization', None),
		('-w', '--writedirpath', str, 'directory path resulting image shall be written to, defaults to dir original image residing at', None),
		include_dir_argument=True
	)

	# parse args
	FILE_PATH = args.path
	DIRECTORY_PATH = args.dir
	N_CLUSTERS = args.clusters
	MAX_ITERATIONS = args.maxiterations
	SEED = args.seed
	WRITE_DIR_PATH = args.writedirpath

	run(main, file_path=FILE_PATH, directory_path=DIRECTORY_PATH)
