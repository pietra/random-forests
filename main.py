import sys

import pandas
from anytree import Node

from dataset_reader import read_dataset
from util import write_tree_on_file, print_tree, read_attributes_type
from decision_tree import decision_tree, classify_instances
from ensemble import create_bootstraps
from cross_validation import cross_validation


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

    mean_f1_measure = cross_validation(
        dataset, number_of_trees, attributes, attributes_types, use_sample_attributes)

    print("---------------------")
    print("Mean F1-Measure: {}".format(mean_f1_measure))
    print("---------------------")


if __name__ == "__main__":
    main()
