from anytree import RenderTree

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