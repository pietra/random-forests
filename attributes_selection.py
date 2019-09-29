import math

from dataset_reader import read_dataset


def id3_algorithm(dataset, attributes):
    gain_information = 0
    choosen_attribute = None
    for attribute in attributes:
        new_gain_information = gain_information_of_attribute(
            dataset, attribute)
        if gain_information <= new_gain_information:
            gain_information = new_gain_information
            choosen_attribute = attribute

    return choosen_attribute


def gain_information_of_attribute(dataset, attribute):
    gain_information = 0
    entropy_dataset = entropy(dataset)
    values_of_attribute_repeated = dataset[attribute].values.tolist()

    values_of_attribute = remove_repeated_values_of_list(
        values_of_attribute_repeated)

    for a_value in values_of_attribute:
        instances = len(dataset[dataset[attribute] == a_value])
        probability_of_value = instances / len(dataset)

        dataset_with_value = dataset[dataset[attribute] == a_value]
        gain_information = gain_information + (probability_of_value *
                                               entropy(dataset_with_value))
    return entropy_dataset - gain_information


def entropy(dataset):
    entropy = 0
    values_of_class = dataset["class"].values.tolist()
    classes = remove_repeated_values_of_list(values_of_class)
    for a_class in classes:
        instances = len(dataset[dataset['class'] == a_class])
        probability_of_class = instances / len(values_of_class)
        entropy = entropy + (probability_of_class *
                             math.log2(probability_of_class))

    return -entropy


def remove_repeated_values_of_list(list_of_values):
    return list(dict.fromkeys(list_of_values))
