import numpy as np
from matplotlib import pyplot as plt
import numba as nb
from numba.experimental import jitclass


spec = [
    ('L', nb.int16),
    ('grid', nb.int8[:]),
    ('step', nb.int16),
    ('grains', nb.int16),
    ('size_array', nb.int32[:]),
    ('critical_value_options', nb.int8[:])
]


@jitclass(spec)
class OsloModelNumba:
    def __init__(self, L: nb.int16 = 10, grains: nb.int16 = 10, threshold: tuple[nb.int8] = (1, 2)):
        self.L = L
        self.grid = np.zeros(self.L, dtype=nb.int8)
        self.step = 0
        self.grains = grains
        self.size_array = np.zeros(grains, dtype=nb.int32)
        self.critical_value_options = np.array(threshold, dtype=nb.int8)

    def reset_parameters(self) -> None:
        self.grid = np.zeros(self.L, dtype=nb.int8)
        self.step = 0
        self.size_array = np.zeros(self.grains, dtype=nb.int32)

    def _increment_top_left(self) -> None:
        self.grid[0] += 1

    def _increment_randomly(self) -> None:
        self.grid[np.random.choice(self.L)] += 1

    def single_relaxation(self, thresholds: nb.int8) -> nb.int32:
        size = 0
        for index, site in enumerate(self.grid):
            if site >= thresholds[index]:
                size += 1
                if self.L - 1 > index > 0:
                    self.grid[index] -= 2
                    self.grid[index + 1] += 1
                    self.grid[index - 1] += 1
                elif site == 0:
                    self.grid[index] -= 2
                    self.grid[index + 1] += 1
                else:
                    self.grid[index] -= 2
                    self.grid[index - 1] += 1
        return size

    def system_relaxation(self) -> None:
        thresholds = np.random.choice(self.critical_value_options, size=self.L).astype(nb.int8)
        avalanche_total_size = 0
        while True:
            avalanche_size = self.single_relaxation(thresholds)
            if avalanche_size == 0:
                break
            else:
                avalanche_total_size += avalanche_size
        self.size_array[self.step] = avalanche_total_size
        self.step += 1

    def add_all_grains(self, random_increment: nb.boolean) -> None:
        self.reset_parameters()
        for _ in range(self.grains):
            if random_increment:
                self._increment_randomly()
            else:
                self._increment_top_left()
            self.system_relaxation()

    def get_plot_data(self) -> tuple[nb.int32[:], nb.int32[:]]:
        return np.arange(1, self.grains + 1), self.size_array


if __name__ == '__main__':
    model: OsloModelNumba = OsloModelNumba(L=200, grains=1000)
    model.add_all_grains(True)

    figure, axes = plt.subplots(figsize=(18, 6))
    axes.stem(np.arange(model.grains), model.size_array)
    plt.show()

