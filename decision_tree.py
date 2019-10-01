import sys
import statistics
import random
import math

from collections import Counter
from anytree import Node

from dataset_reader import read_dataset
from util import write_tree_on_file, print_tree, read_attributes_type, find_attribute_type, calculate_median_of_attribute, remove_repeated_values_of_list
from attributes_selection import id3_algorithm


def decision_tree(dataset, attributes, attributes_types, use_sample_attributes, father=None):
    some_class = is_dataset_with_only_one_class(dataset)
    if some_class:
        Node(some_class, parent=father)

    elif not attributes:
        classes = dataset["class"].values.tolist()
        Node(return_most_common_value(classes), parent=father)

    else:
        if(use_sample_attributes == 'sim'):
            attributes_sample = create_sample_of_attributes(attributes)
            attribute = id3_algorithm(
                dataset, attributes_sample, attributes_types)
        else:
            attribute = id3_algorithm(dataset, attributes, attributes_types)
        attributes.remove(attribute)

        new_node = Node(attribute, parent=father)

        attribute_type = find_attribute_type(attribute, attributes_types)
        if(attribute_type == 'categorico'):
            values_of_that_attribute = remove_repeated_values_of_list(
                dataset[attribute].values.tolist())

            # For each value of that attribute
            for value in values_of_that_attribute:
                dataset_filtered_by_value = dataset[dataset[attribute] == value]
                create_value_node(
                    value, new_node, dataset_filtered_by_value, dataset, attributes, attributes_types, use_sample_attributes)

        else:
            median = calculate_median_of_attribute(dataset, attribute)

            # node with value <= median
            dataset_filtered_by_value = dataset[dataset[attribute] <= median]
            value = '<= ' + str(median)
            create_value_node(value, new_node, dataset_filtered_by_value,
                              dataset, attributes, attributes_types, use_sample_attributes)

            # node with value > median
            dataset_filtered_by_value = dataset[dataset[attribute] > median]
            value = '> ' + str(median)
            create_value_node(value, new_node, dataset_filtered_by_value,
                              dataset, attributes, attributes_types, use_sample_attributes)

        return new_node


def create_value_node(value, new_node, dataset_filtered_by_value, dataset, attributes, attributes_types, use_sample_attributes):
    value_node = Node(value, parent=new_node)

    # There are no instances for that value
    if dataset_filtered_by_value.empty:
        classes = dataset["class"].values.tolist()
        Node(return_most_common_value(classes), parent=value_node)
    else:
        decision_tree(
            dataset_filtered_by_value, attributes, attributes_types, use_sample_attributes, value_node)


def is_dataset_with_only_one_class(dataset):
    if not dataset.empty:
        some_class = dataset['class'].tolist()[0]
        for index, row in dataset.iterrows():
            if dataset.at[index, 'class'] != some_class:
                return False
        return some_class
    return False


def return_most_common_value(a_list):
    occurence_count = Counter(a_list)
    return occurence_count.most_common(1)[0][0]


def create_sample_of_attributes(attributes):
    attributes_sample = []
    square = int(math.sqrt(len(attributes)))
    for i in range(square):
        attributes_sample.append(random.choice(attributes))

    return attributes_sample
