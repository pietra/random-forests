from dataclasses import dataclass


@dataclass
class Leaf:
    which_class: str
    value: str

    def __init__(self, which_class=None, value=None):
        self.which_class = which_class
        self.value = value

    def print_leaf(self, level=0):
        hifen = ""
        for i in range(level):
            hifen = hifen + "-----"
        print(hifen, "which_class: ", self.which_class, ", value: ", self.value)


@dataclass
class Node:
    attribute: str
    children: list

    def __init__(self, value=None, attribute=None):
        self.attribute = attribute
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_node(self, level=0):
        hifen = ""
        for i in range(level):
            hifen = hifen + "-----"
        print(hifen, "attribute: ", self.attribute)
        print(hifen, "children: ")
        for child in self.children:
            if(isinstance(child, Node)):
                print(child.print_node(level+1))
            else:
                print(child.print_leaf(level+1))
