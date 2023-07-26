import random
from functools import cached_property

from utils import Log

log = Log('Population')


class Population:
    def __init__(self, wealth_list):
        self.wealth_list = wealth_list

    @staticmethod
    def gen_random():
        N_POPULATION = 5
        while True:
            i_list = [random.random() for _ in range(N_POPULATION)]
            if sum(i_list) > 0:
                sum_i_list = sum(i_list)
                wealth_list = [
                    i_list[i] / sum_i_list for i in range(N_POPULATION)
                ]
                return Population(wealth_list)

    @cached_property
    def total_wealth(self):
        return sum(self.wealth_list)

    @cached_property
    def gini(self):
        n = len(self)
        wealth_list = sorted(self.wealth_list)
        numerator = 0
        for i, wealth in enumerate(wealth_list):
            numerator += (2 * i - n + 1) * wealth
        return numerator / (n * self.total_wealth)

    @cached_property
    def envy(self):
        n = len(self)
        n_envy = 0
        for i1 in range(n):
            for i2 in range(n):
                if self.wealth_list[i2] > self.wealth_list[i1] * 2:
                    n_envy += 1
        n_pairs = n**2
        return n_envy / n_pairs

    def __str__(self):
        wealth_list_str = ', '.join(
            f'{w:.0%}' for w in sorted(self.wealth_list)
        )
        return '\n'.join(
            [
                f'Population(n={len(self)}, wealth={self.total_wealth:.1f}, '
                + f'Gini={self.gini:.0%}, envy={self.envy:.0%})',
                wealth_list_str,
            ]
        )

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.wealth_list)


if __name__ == '__main__':
    N_POPULATION_LIST = 10**6
    population_list = [
        Population.gen_random() for _ in range(N_POPULATION_LIST)
    ]

    high_gini = [
        population
        for population in population_list
        if 0.5 < population.gini > 0.55
    ]
    by_envy = sorted(high_gini, key=lambda p: p.envy)
    n2 = len(by_envy) // 2
    print(by_envy[0])
    print(by_envy[n2 // 4])
    print(by_envy[-n2 // 4])
    print(by_envy[-1])
