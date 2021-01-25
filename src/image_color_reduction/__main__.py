""" Reduce quantity of colors present in image by means of kMeans clustering the entirety
	of rgb values present in the original image and subsequently assigning the image
	pixels with the cluster means they ended up in.
	Original file will be left untouched while the thus created image will be written to
	the directory, the former is residing in.

	Refer to the bottom of this file in order to read up on the passable cli options. """

import cv2

from src.image_color_reduction import get_indexed_pixels, get_write_path, restore_image
from src.image_color_reduction._k_means_clustering import KMeansClusterer


def main(image_file_path: str):
	# open image and get indexed, sequentialized pixels
	original_image = cv2.imread(image_file_path)
	indexed_pixels = get_indexed_pixels(original_image)

	# cluster rgb values being present in image
	clusterer = KMeansClusterer(indexed_pixels, N_CLUSTERS, max_iterations=MAX_ITERATIONS, seed=SEED)
	clusters = clusterer()

	# write color reduced image
	write_path = get_write_path(image_file_path, WRITE_DIR_PATH, n_clusters=N_CLUSTERS, conducted_iterations=clusterer.n_conducted_iterations)
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
