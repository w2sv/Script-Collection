from typing import Tuple, List
import os

from tqdm import tqdm
import numpy as np
import cv2

from src.utils import kick_off_message_displayer
from src.image_color_reduction.k_means_clustering import KMeansClusterer


class IndexedPixel(np.ndarray):
	def __new__(cls, array_like: np.ndarray, indices: Tuple[int, int]):
		obj = array_like.view(cls)
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
def restored_image(pixel_clusters: List[IndexedPixel], image_shape: Tuple[int]) -> np.ndarray:
	image = np.zeros(shape=image_shape)

	for pixel_cluster in tqdm(pixel_clusters):
		cluster_mean = np.mean(pixel_cluster, axis=0)

		for pixel in pixel_cluster:
			image[pixel.indices] = cluster_mean

	return image


def get_write_path(original_path: str, n_clusters: int, conducted_iterations: int) -> str:
	extension_stripped_path, extension = os.path.splitext(original_path)
	suffix = f'_{n_clusters}clusters_{conducted_iterations}iterations' + extension

	if write_dir_path is None:
		return extension_stripped_path + suffix

	file_name = original_path.split(os.sep)[-1]
	return os.path.join(write_dir_path, file_name + suffix)


def main(image_file_path: str):
	# open, sequentialize image
	original_image = cv2.imread(image_file_path)
	indexed_pixels = get_indexed_pixels(original_image)

	# cluster
	clusterer = KMeansClusterer(indexed_pixels, n_clusters, max_iterations=max_iterations, seed=seed)
	clusters = clusterer.__call__()

	# write color reduced image
	write_path = get_write_path(image_file_path, n_clusters=n_clusters, conducted_iterations=clusterer.n_conducted_iterations)
	cv2.imwrite(write_path, restored_image(clusters, image_shape=original_image.shape))
	print(f'Saved color reduced image to {write_path}')


if __name__ == '__main__':
	from src.utils import parse_args
	from src import run

	args = parse_args(
		('-p', '--path', str, 'image path', None),
		('-d', '--dir', str, 'directory path', None),
		('-c', '--clusters', int, 'number of desired colors image colors will be reduced to', 10),
		('-m', '--maxiterations', int, 'maximal amount of conducted kMeans clustering iterations', 5),
		('-s', '--seed', int, 'rng seed, affects centroid initialization', None),
		('-w', '--writedirpath', str, 'directory path resulting image shall be written to, defaults to dir original image residing at', None)
	)

	# parse args
	file_path = args.path
	directory_path = args.dir
	n_clusters = args.clusters
	max_iterations = args.maxiterations
	seed = args.seed
	write_dir_path = args.writedirpath

	run.__call__(main, file_path=file_path, directory_path=directory_path)
