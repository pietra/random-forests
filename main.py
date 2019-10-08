import sys

from anytree import Node

from dataset_reader import read_dataset
from util import write_tree_on_file, print_tree, read_attributes_type
from decision_tree import decision_tree, classify_instances
from ensemble import create_bootstraps


def main():
    print("Starting Random Forests Algorithm...")

    # 1st parameter: dataset.csv
    # 2nd parameter: dataset_config.txt
    # 3rd parameter: use sample of attributes when choosing next attribute to split?
    # 4th parameter: how many trees?
    dataset, attributes = read_dataset(sys.argv[1])
    attributes_types = read_attributes_type(sys.argv[2])
    use_sample_attributes = sys.argv[3]
    number_of_trees = int(sys.argv[4])

    attributes.remove('class')

    # Ensemble:
    bootstraps, training_sets = create_bootstraps(dataset, number_of_trees)
    trees = []

    for i in range(number_of_trees):
        tree = Node("Decision Tree {}".format(i))
        final_decision_tree = decision_tree(
            dataset, bootstraps[i], attributes[:], attributes_types, use_sample_attributes, tree)
        trees.append(final_decision_tree)

    classes = classify_instances(dataset, trees)

    for tree in trees:
        print_tree(tree)

    #write_tree_on_file(final_decision_tree)


if __name__ == "__main__":
    main()
