import pandas as pd

from util import remove_repeated_values_of_list


def create_bootstraps(dataset, n_bootstraps):
    bootstraps = initialize_set(n_bootstraps)
    training_sets = initialize_set(n_bootstraps)

    for i in range(n_bootstraps):
        for j in range(len(dataset)):
            random_instance = dataset.sample(n=1)
            if bootstraps[i] is None:
                bootstraps[i] = pd.DataFrame(random_instance)
            else:
                bootstraps[i] = bootstraps[i].append(random_instance)
    return bootstraps


def initialize_set(n):
    a_set = []
    for i in range(n):
        a_set.append(None)
    return a_set
