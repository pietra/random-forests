import pandas as pd

from util import remove_repeated_values_of_list


def create_bootstraps(dataset, n):
    bootstraps = initialize_set(n)
    training_sets = initialize_set(n)

    for i in range(n):
        selected_instances = []

        for j in range(len(dataset)):
            random_instance = dataset.sample(n=1)
            if bootstraps[i] is None:
                bootstraps[i] = pd.DataFrame(random_instance)
            else:
                bootstraps[i] = bootstraps[i].append(random_instance)
            selected_instances.append(random_instance.index[0])

        all_instances = [j for j in range(len(dataset))]
        not_selected_instances = set(all_instances) - set(selected_instances)

        for instance_id in not_selected_instances:
            instance = dataset.iloc[[instance_id]]
            if training_sets[i] is None:
                training_sets[i] = pd.DataFrame(instance)
            else:
                training_sets[i] = training_sets[i].append(instance)

    return bootstraps, training_sets


def initialize_set(n):
    a_set = []
    for i in range(n):
        a_set.append(None)
    return a_set
