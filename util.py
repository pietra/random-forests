import statistics

from anytree import RenderTree

from dataclasses import dataclass


@dataclass
class Attribute:
    name: str
    type_of: str


def print_tree(tree):
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))


def write_tree(f, tree):
    for pre, fill, node in RenderTree(tree):
        f.write("%s%s\n" % (pre, node.name))


def write_tree_on_file(tree):
    f = open("tree.txt", "w+")
    write_tree(f, tree)
    f.close()


def read_attributes_type(f_path):
    attributes_types = []

    f = open(f_path, "r")
    for line in f:
        values = line.split()
        attributes_types.append(Attribute(values[0], values[1]))
    f.close()

    return attributes_types


def remove_repeated_values_of_list(list_of_values):
    return list(dict.fromkeys(list_of_values))


def find_attribute_type(attribute, attributes_types):
    for attribute_type in attributes_types:
        if attribute_type.name == attribute:
            return attribute_type.type_of


def calculate_median_of_attribute(dataset, attribute):
    attribute_column = dataset[attribute]
    return statistics.mean(attribute_column)
