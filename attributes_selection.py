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

    values_of_attribute = remove_repeated_values_of_list(
        dataset[attribute].values.tolist())
    for a_value in values_of_attribute:
        dataset_with_value = dataset[dataset[attribute] == a_value]
        probability_of_value = len(dataset_with_value) / len(dataset)
        gain_information = gain_information + (probability_of_value *
                                               entropy(dataset_with_value))
    return entropy_dataset - gain_information


def entropy(dataset):
    entropy = 0
    classes = remove_repeated_values_of_list(dataset["class"].values.tolist())
    for a_class in classes:
        dataset_with_a_class = dataset[dataset['class'] == a_class]
        probability_of_class = len(dataset_with_a_class) / len(dataset)
        entropy = entropy + (probability_of_class *
                             math.log2(probability_of_class))

    return -entropy


def remove_repeated_values_of_list(list_of_values):
    return list(dict.fromkeys(list_of_values))
