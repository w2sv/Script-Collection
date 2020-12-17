from typing import Sequence, List, Optional
import itertools

from tqdm import tqdm
import numpy as np


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a - b)


def ordinal_number(number: int) -> str:
    """ Source: Gareth @ https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712 """

    return "%d%s" % (number, "tsnrhtdd"[(number // 10 % 10 != 1) * (number % 10 < 4) * number % 10::4])


class KMeansClusterer:
    _Clusters = List[List[np.ndarray]]

    def __init__(self, data: Sequence[np.ndarray], n_clusters: int, max_iterations=20):
        self._data: Sequence[np.ndarray] = data
        self._n_clusters: int = n_clusters
        self._recursion_threshold: int = max_iterations

        self._centroids: List[np.ndarray] = self._sample_distinct_random_data_points(data, n=n_clusters)

        self._progress_bar = tqdm(total=self._recursion_threshold)
        self.n_conducted_iterations: int = 0

    @staticmethod
    def _sample_distinct_random_data_points(data: Sequence[np.ndarray], n: int) -> List[np.ndarray]:
        indices = np.arange(len(data))
        np.random.shuffle(indices)
        return np.array_split(np.array(data)[indices[:n]], n, axis=0)

    def __call__(self, previous_clusters: Optional[_Clusters] = None) -> _Clusters:
        new_clusters = self._get_clusters()
        self._adjust_centroids(new_clusters)

        if previous_clusters is None or (self._clusters_divergent(previous_clusters, new_clusters) and self.n_conducted_iterations < self._recursion_threshold):
            return self.__call__(new_clusters)

        print(f'Finished after {self.n_conducted_iterations + 1} iterations')
        return new_clusters

    def _get_clusters(self) -> _Clusters:
        self._progress_bar.set_description(f'Conducting {ordinal_number(self.n_conducted_iterations + 1)} iteration', refresh=True)

        clusters = [[] for _ in range(self._n_clusters)]
        for data_point in self._data:
            corresponding_centroid_distances = list(map(lambda centroid: euclidean_distance(data_point, centroid), self._centroids))
            clusters[np.argmin(corresponding_centroid_distances)].append(data_point)

        self._progress_bar.update(1)
        self.n_conducted_iterations += 1

        return clusters

    def _adjust_centroids(self, clusters: _Clusters):
        self._centroids = [np.mean(cluster, axis=0) for cluster in clusters]

    @staticmethod
    def _clusters_divergent(previous_clusters: _Clusters, new_clusters: _Clusters) -> bool:
        for previous_cluster_i, new_cluster_i in itertools.zip_longest(previous_clusters, new_clusters):
            if not np.array_equal(previous_cluster_i, new_cluster_i):
                return True
        return False


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    example_data = np.random.randint(0, 100, (50, 2))
    clusterer = KMeansClusterer(example_data, n_clusters=3, max_iterations=5)
    clusters = clusterer.__call__()

    # for cluster in clusters:
    #     plt.scatter(*cluster.T)
    #
    # plt.show()