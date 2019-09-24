from dataset_reader import read_dataset
from collections import Counter
import random

from anytree import Node, RenderTree


def main():
    dataset, attributes = read_dataset("dataset_joga_tenis.csv")
    attributes.remove('class')
    tree = Node("Decision Tree")
    final_decision_tree = decision_tree(dataset, attributes, tree)
    print_tree(final_decision_tree)


def decision_tree(dataset, attributes, father=None):
    # Only one class for that dataset
    some_class = only_one_class(dataset)
    if some_class:
        Node(some_class, parent=father)

    # No more attributes
    elif not attributes:
        classes = dataset["class"].values.tolist()
        Node(most_frequent(classes), parent=father)

    else:
        # Choose a attribute
        attribute = random.choice(attributes)  # TODO: choice can't be random
        attributes.remove(attribute)
        values_of_that_attribute = dataset[attribute].values.tolist()
        values_of_that_attribute = remove_repeated_values_of_list(
            values_of_that_attribute)

        # Create attribute node
        new_node = Node(attribute, parent=father)

        # For each value of that attribute
        for value in values_of_that_attribute:
            dataset_filtered_by_value = dataset[dataset[attribute] == value]
            value_node = Node(value, parent=new_node)
            # If there are no cases for that value
            if dataset_filtered_by_value.empty:
                classes = dataset["class"].values.tolist()
                Node(most_frequent(classes), parent=value_node)
            else:
                decision_tree(
                    dataset_filtered_by_value, attributes, value_node)
        return new_node


def only_one_class(dataset):
    if not dataset.empty:
        some_class = dataset['class'].tolist()[0]
        for index, row in dataset.iterrows():
            if dataset.at[index, 'class'] != some_class:
                return False
        return some_class
    return False


def remove_repeated_values_of_list(list_of_values):
    return list(dict.fromkeys(list_of_values))


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


def print_tree(tree):
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))


if __name__ == "__main__":
    main()
