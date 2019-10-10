import math
import statistics

import pandas as pd
from anytree import Node

from util import remove_repeated_values_of_list
from decision_tree import decision_tree, classify_instances
from ensemble import create_bootstraps

FOLDS_NUMBER = 5


def cross_validation(dataset, number_of_trees, attributes, attributes_types, use_sample_attributes):

    classes = remove_repeated_values_of_list(dataset["class"].values.tolist())
    dataset_by_class = organize_dataset_by_class(dataset, classes)
    folds = create_folds(classes, dataset_by_class, FOLDS_NUMBER)

    f1_measures = []
    for i in range(FOLDS_NUMBER):
        training_set = create_training_set(folds, i)
        # Shuffle dataset
        training_set = training_set.sample(frac=1)

        bootstraps = create_bootstraps(training_set, number_of_trees)

        trees = []
        for j in range(number_of_trees):
            tree = Node("Decision Tree {}".format(i))
            final_decision_tree = decision_tree(
                dataset, bootstraps[j], attributes[:], attributes_types, use_sample_attributes, tree)
            trees.append(final_decision_tree)

        classes_predicted = classify_instances(folds[i], trees)

        f1_measure = calculate_f1_measure(classes_predicted, classes, folds[i])
        f1_measures.append(f1_measure)

    return statistics.mean(f1_measures)


def calculate_f1_measure(classes_predicted, classes, dataset):
    true_positives, false_negatives, false_positives = calculate_confusion_matrix(
        dataset, classes, classes_predicted)

    precision = calculate_precision(true_positives, false_positives)
    recall = calculate_recall(true_positives, false_negatives)

    if precision + recall > 0:
        return 2 * precision * recall / (precision + recall)
    else:
        return 0


def calculate_confusion_matrix(dataset, classes, classes_predicted):
    true_positives = {}
    false_negatives = {}
    false_positives = {}

    for a_class in classes:
        i = 0
        for index, row in dataset.iterrows():
            correct_class = row['class']
            evaluted_class = a_class
            if evaluted_class == classes_predicted[i]:
                # VP
                if evaluted_class == correct_class:
                    if evaluted_class not in true_positives:
                        true_positives[evaluted_class] = 1
                    else:
                        true_positives[evaluted_class] += 1
                # FN
                else:
                    if evaluted_class not in false_positives:
                        false_positives[evaluted_class] = 1
                    else:
                        false_positives[evaluted_class] += 1
            elif evaluted_class == correct_class:
                if evaluted_class not in false_negatives:
                    false_negatives[evaluted_class] = 1
                else:
                    false_negatives[evaluted_class] += 1
            i += 1

    return true_positives, false_negatives, false_positives


def calculate_precision(true_positives, false_positives):
    total_true_positives = sum(true_positives.values())
    total_false_positives = sum(false_positives.values())
    if (total_true_positives + total_false_positives) > 0:
        return total_true_positives / (total_true_positives + total_false_positives)
    else:
        return 0


def calculate_recall(true_positives, false_negatives):
    total_true_positives = sum(true_positives.values())
    total_false_negatives = sum(false_negatives.values())
    if (total_true_positives + total_false_negatives) > 0:
        return total_true_positives / (total_true_positives + total_false_negatives)
    else:
        return 0


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
        dataset_with_class = dataset_by_class[a_class]
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


def organize_dataset_by_class(dataset, classes):
    dictionary = {}
    for class_a in classes:
        dictionary[class_a] = None

    
    for index, row in dataset.iterrows():
        row_class = row['class']
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
