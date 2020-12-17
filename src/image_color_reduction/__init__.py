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
def restored_image(pixel_clusters: List[IndexedPixel]) -> np.ndarray:
	image = np.zeros(shape=original_image.shape)

	for pixel_cluster in tqdm(pixel_clusters):
		cluster_mean = np.mean(pixel_cluster, axis=0)

		for pixel in pixel_cluster:
			image[pixel.indices] = cluster_mean

	return image


def get_write_path(original_path: str, n_clusters: int, conducted_iterations: int) -> str:
	extension_stripped_path, extension = os.path.splitext(original_path)
	return extension_stripped_path + f'_{n_clusters}clusters_{conducted_iterations}iterations' + extension


if __name__ == '__main__':
	from src.utils import parse_args

	args = parse_args(
		('-p', '--path', str, 'image path', None),
		('-c', '--clusters', int, 'number of desired colors image colors will be reduced to', 10),
		('-m', '--maxiterations', int, 'maximal amount of conducted kMeans clustering iterations', 5)
	)

	# parse args
	image_path = args.path
	n_clusters = args.clusters
	max_iterations = args.maxiterations

	# open, sequentialize image
	original_image = cv2.imread(image_path)
	indexed_pixels = get_indexed_pixels(original_image)

	# cluster
	clusterer = KMeansClusterer(indexed_pixels, n_clusters, max_iterations=max_iterations)
	clusters = clusterer.__call__()

	# write color reduced image
	write_path = get_write_path(image_path, n_clusters=n_clusters, conducted_iterations=clusterer.n_conducted_iterations)
	cv2.imwrite(write_path, restored_image(clusters))
	print(f'Saved color reduced image to {write_path}')
