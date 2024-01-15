import numpy as np
from matplotlib import pyplot as plt


class OsloModel:
    def __init__(self, L=10, grains=10):
        self.L = L
        self.grid = np.zeros(self.L, dtype=np.int8)
        self.step = 0
        self.grains = grains
        self.size_array = np.zeros(grains, dtype=np.int32)
        self.critical_value_options = np.array([1, 2], dtype=np.int8)

    def reset_parameters(self):
        self.grid = np.zeros(self.L, dtype=np.int8)
        self.step = 0
        self.size_array = np.zeros(self.grains, dtype=np.int32)

    def _increment_top_left(self):
        self.grid[0] += 1

    def _increment_randomly(self):
        self.grid[np.random.choice(self.L)] += 1

    def system_relaxation(self):
        thresholds = np.random.choice(self.critical_value_options, size=self.L)
        avalanche_total_size = 0
        while True:
            avalanche_size = self.single_relaxation(thresholds)
            # print(avalanche_size)
            # print(thresholds)
            # print(self.grid)
            if avalanche_size == 0:
                break
            else:
                avalanche_total_size += avalanche_size
        self.size_array[self.step] = avalanche_total_size
        self.step += 1

    def single_relaxation(self, thresholds):
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

    def add_all_grains(self, random_increment=False):
        self.reset_parameters()
        for _ in range(self.grains):
            if random_increment:
                self._increment_randomly()
            else:
                self._increment_top_left()
            self.system_relaxation()


if __name__ == '__main__':
    model = OsloModel(L=100, grains=1000)
    model.add_all_grains(random_increment=True)

    figure, axes = plt.subplots()
    axes.scatter(np.arange(model.grains), model.size_array)
    plt.show()

