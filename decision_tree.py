from dataset_reader import read_dataset
from treelib import Tree, Node
import statistics
from statistics import mode
import random


def main():
    dataset, attributes = read_dataset("dataset_31_credit-g.csv")
    attributes.remove('class')
    tree = Tree()
    decision_tree(dataset, attributes, tree)
    tree.show()


def decision_tree(dataset, attributes, tree, value=None):
    # Only one class for that dataset
    some_class = only_one_class(dataset)
    if some_class:
        breakpoint()
        return tree.create_node(some_class, some_class, parent=value)

    # No more attributes
    elif not attributes:
        classes = dataset["class"].values.tolist()
        breakpoint()
        return tree.create_node(mode(classes), mode(classes), parent=value)

    else:
        # Choose a attribute
        attribute = random.choice(attributes)  # TODO: choice can't be random
        attributes.remove(attribute)
        values_of_that_attribute = dataset[attribute].values.tolist()
        values_of_that_attribute = remove_repeated_values_of_list(
            values_of_that_attribute)

        # Subtree
        new_tree = Tree()
        new_tree.create_node(attribute, attribute)

        # For each value of that attribute
        for value in values_of_that_attribute:

            new_tree.create_node(value, value, parent=attribute)

            dataset_filtered_by_value = dataset[dataset[attribute] == value]
            # If there are no cases for that value
            if dataset_filtered_by_value.empty:
                classes = dataset["class"].values.tolist()
                breakpoint()
                return new_tree.create_node(mode(classes), mode(classes), parent=value)
            else:
                decision_tree(
                    dataset_filtered_by_value, attributes, new_tree, value)
        breakpoint()
        #tree.create_node(attribute, parent=1)
        return tree.paste(attribute, new_tree)


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


if __name__ == "__main__":
    main()
