import numpy as np
from matplotlib import pyplot as plt


class OsloModel:
    def __init__(self, L=10, grains=10, threshold=(1, 2)):
        self.L = L
        self.grid = np.zeros(self.L, dtype=np.int8)
        self.step = 0
        self.grains = grains
        self.size_array = np.zeros(grains, dtype=np.int32)
        self.critical_value_options = np.array(threshold, dtype=np.int8)

    def get_current_grid(self):
        return self.grid

    def reset_parameters(self):
        self.grid = np.zeros(self.L, dtype=np.int8)
        self.step = 0
        self.size_array = np.zeros(self.grains, dtype=np.int32)

    def increment_top_left(self):
        self.grid[0] += 1

    def increment_randomly(self):
        self.grid[np.random.choice(self.L)] += 1

    def single_relaxation(self, thresholds):
        size = 0
        for index, site in enumerate(self.grid):
            if site >= thresholds[index]:
                size += 1
                if self.L - 1 > index > 0:
                    self.grid[index] -= 2
                    self.grid[index + 1] += 1
                    self.grid[index - 1] += 1
                elif index == 0:
                    self.grid[index] -= 2
                    self.grid[index + 1] += 1
                else:
                    self.grid[index] -= 2
                    self.grid[index - 1] += 1
        return size

    def system_relaxation(self):
        # print(f'options {self.critical_value_options}')
        thresholds = np.random.choice(self.critical_value_options, size=self.L).astype(np.int8)
        # print(f'thres {thresholds}')
        avalanche_total_size = 0
        while True:
            avalanche_size = self.single_relaxation(thresholds)
            if avalanche_size == 0:
                break
            else:
                avalanche_total_size += avalanche_size
        self.size_array[self.step] = avalanche_total_size
        self.step += 1

    def add_all_grains(self, random_increment=False):
        self.reset_parameters()
        for _ in range(self.grains):
            if random_increment:
                self.increment_randomly()
            else:
                self.increment_top_left()
            self.system_relaxation()

    def get_plot_data(self):
        return np.arange(1, self.grains), self.size_array


if __name__ == '__main__':
    L = 10
    grains = 10
    is_random = False
    model = OsloModel(L=L, grains=grains, threshold=tuple([1, 2]))
    print(model.get_current_grid())
    for _ in range(grains):
        if is_random:
            model.increment_randomly()
        else:
            model.increment_top_left()
        print(f'bef {model.grid}')
        model.system_relaxation()
        print(f'aft {model.grid}')
