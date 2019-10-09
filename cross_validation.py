import math

import pandas as pd
from anytree import Node

from util import remove_repeated_values_of_list
from decision_tree import decision_tree, classify_instances
from ensemble import create_bootstraps


def cross_validation(dataset, number_of_trees, attributes, attributes_types, use_sample_attributes):
    classes = remove_repeated_values_of_list(dataset["class"].values.tolist())
    dataset_by_class = organize_dataset_by_class(dataset)
    folds = create_folds(classes, dataset_by_class, number_of_trees)

    accuracies = []
    for i in range(len(folds)):
        training_set = create_training_set(folds, i)
        bootstraps = create_bootstraps(training_set, number_of_trees)

        trees = []
        for i in range(number_of_trees):
            tree = Node("Decision Tree {}".format(i))
            final_decision_tree = decision_tree(
                dataset, bootstraps[i], attributes[:], attributes_types, use_sample_attributes, tree)
            trees.append(final_decision_tree)

        classes_predicted = classify_instances(folds[i], trees)

        accuracy = calculate_accuracy(classes_predicted, folds[i])
        accuracies.append(accuracy)

    return accuracies


def calculate_accuracy(classes_predicted, dataset):
    true_positives = 0
    i = 0
    for index, row in dataset.iterrows():
        if eval(row['class']) == classes_predicted[i]:
            true_positives += 1
        i += 1
    return true_positives / len(dataset)


def create_training_set(folds, test_fold_index):
    training_set = None
    for i in range(len(folds)):
        if i is not test_fold_index:
            if training_set is None:
                training_set = folds[i]
            else:
                training_set = training_set.append(folds[i])
    return training_set


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
