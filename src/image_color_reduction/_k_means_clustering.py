from typing import Sequence, List, Optional
import itertools

from tqdm import tqdm
import numpy as np


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a - b)


def ordinal_number(number: int) -> str:
    """ Source: Gareth @ https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712

    >>>ordinal_number(1)
    '1st'
    >>>ordinal_number(2)
    '2nd'
    >>>ordinal_number(4)
    '4th' """

    return "%d%s" % (number, "tsnrhtdd"[(number // 10 % 10 != 1) * (number % 10 < 4) * number % 10::4])


class KMeansClusterer:
    _Cluster = List[np.ndarray]
    _ClusterComposition = List[_Cluster]

    def __init__(self,
                 data: Sequence[np.ndarray],
                 n_clusters: int,
                 max_iterations=20,
                 seed: Optional[int] = None):

        # set seed if passed
        if seed:
            np.random.seed(seed)

        self._data: Sequence[np.ndarray] = data
        self._n_clusters: int = n_clusters
        self._max_iterations: int = max_iterations

        # initialize centroids randomistically
        self._centroids: List[np.ndarray] = self._unique_random_samples(data, n=n_clusters)

        self._progress_bar = tqdm(total=self._max_iterations)
        self.n_conducted_iterations: int = 0

    @staticmethod
    def _unique_random_samples(data: Sequence[np.ndarray], n: int) -> List[np.ndarray]:
        indices = np.arange(len(data))
        np.random.shuffle(indices)
        return np.array_split(np.array(data)[indices[:n]], n, axis=0)

    def __call__(self, _previous_clusters: Optional[_ClusterComposition] = None) -> _ClusterComposition:
        """ Conduct kMeans clustering iterations, until either no data point assignment
            change having taken place throughout clustering with respect to the
            corresponding previous cluster composition, or number of max iterations
            reached

            Args:
                _previous_clusters: recursion arg, not to be passed at invocation """

        if _previous_clusters is not None:
            self._adjust_centroids(_previous_clusters)

        new_clusters = self._cluster()

        if _previous_clusters is None or (self._clusters_divergent(_previous_clusters, new_clusters) and self.n_conducted_iterations < self._max_iterations):
            return self.__call__(new_clusters)

        print(f'Finished after {self.n_conducted_iterations} iterations')
        return new_clusters

    def _cluster(self) -> _ClusterComposition:
        self._progress_bar.set_description(f'Conducting {ordinal_number(self.n_conducted_iterations + 1)} clustering iteration', refresh=True)

        # assign data points to clusters
        clusters = [[] for _ in range(self._n_clusters)]
        for data_point in self._data:
            corresponding_centroid_distances = list(map(lambda centroid: euclidean_distance(data_point, centroid), self._centroids))
            clusters[np.argmin(corresponding_centroid_distances)].append(data_point)

        # increment iteration number monitoring attributes
        self._progress_bar.update(1)
        self.n_conducted_iterations += 1

        return clusters

    def _adjust_centroids(self, clusters: _ClusterComposition):
        self._centroids = [np.mean(cluster, axis=0) for cluster in clusters]

    @staticmethod
    def _clusters_divergent(a: _ClusterComposition, b: _ClusterComposition) -> bool:
        """ Returns True if samples contained within any pair a_i and b_i diverge from
            one another regardless of their indices """

        for ith_clusters in itertools.zip_longest(a, b):
            if not np.array_equal(*map(lambda cluster: np.sort(cluster, axis=0), ith_clusters)):
                return True
        return False


if __name__ == '__main__':
    pass

    # import matplotlib.pyplot as plt

    # example_data = np.random.randint(0, 100, (50, 2))
    # clusterer = KMeansClusterer(example_data, n_clusters=3, max_iterations=5)
    # clusters = clusterer.__call__()

    # for cluster in clusters:
    #     plt.scatter(*cluster.T)
    #
    # plt.show()