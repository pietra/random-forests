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
