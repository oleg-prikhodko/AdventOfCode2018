import re
from collections import defaultdict
from itertools import chain
from string import ascii_uppercase

from day_2 import load_strings

NODE_PATTERN = r"Step (\w) must be finished before step (\w) can begin."


class Graph:
    def __init__(self, root):
        self.root = root


class Node:
    def __init__(self, name, parents, children):
        self.name = name
        self.parents = parents
        self.children = children


def load_nodes(lines):
    childs = defaultdict(list)
    for line in lines:
        match = re.search(NODE_PATTERN, line)
        childs[match.group(1)].append(match.group(2))
    return childs


if __name__ == "__main__":
    nodes_by_parent = load_nodes(load_strings("input_7.txt"))
    parents = set(nodes_by_parent.keys())
    children = set(chain.from_iterable(nodes_by_parent.values()))
    vertices = parents | children
    leaves = parents ^ vertices
    roots = children ^ vertices

    nodes_by_child = defaultdict(list)
    for child in children:
        for node, node_children in nodes_by_parent.items():
            if child in node_children:
                nodes_by_child[child].append(node)

    selection = list(roots)
    result = []
    while selection:
        node = min(selection)
        selection.remove(node)
        result.append(node)

        node_children = nodes_by_parent[node]
        for child in node_children:
            child_parents = set(nodes_by_child[child])
            available_to_add = child_parents.issubset(set(result))
            if available_to_add:
                selection.append(child)
            print()

    print("".join(result))
