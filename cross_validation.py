import math

import pandas as pd

from util import remove_repeated_values_of_list


def cross_validation(dataset, trees):
    classes = remove_repeated_values_of_list(dataset["class"].values.tolist())
    dataset_by_class = organize_dataset_by_class(dataset)
    folds = create_folds(classes, dataset_by_class, len(trees))

    #for fold in folds:

    return 0


def create_folds(classes, dataset_by_class, n_folds):
    folds = initialize_set(n_folds)
    for a_class in classes:
        dataset_with_class = dataset_by_class[eval(a_class)]
        for index_instance in range(len(dataset_with_class)):
            for index_fold in range(n_folds):
                if index_instance < len(dataset_with_class):
                    instance = dataset_with_class.head(1)
                    instance_id = instance.index[0]
                    dataset_with_class = dataset_with_class.drop(instance_id)
                    if folds[index_fold] is None:
                        folds[index_fold] = pd.DataFrame(instance)
                    else:
                        folds[index_fold] = folds[index_fold].append(instance)

    return folds


def organize_dataset_by_class(dataset):
    classes = remove_repeated_values_of_list(dataset["class"].values.tolist())

    dictionary = {}
    for class_a in classes:
        dictionary[eval(class_a)] = None

    for index, row in dataset.iterrows():
        row_class = eval(row['class'])
        if dictionary[row_class] is None:
            dictionary[row_class] = pd.DataFrame([row])
        else:
            dictionary[row_class] = dictionary[row_class].append([row])

    return dictionary


def initialize_set(n):
    a_set = []
    for i in range(n):
        a_set.append(None)
    return a_set
