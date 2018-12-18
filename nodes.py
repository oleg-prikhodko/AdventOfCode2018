import re
from collections import namedtuple

NODE_PATTERN = re.compile(r"(\d+) (\d+)")
Node = namedtuple("Node", "childs metas")

nodes = []


def process(input_string):
    global nodes
    match = re.search(NODE_PATTERN, input_string)
    child_count = int(match.group(1))
    meta_count = int(match.group(2))

    if child_count == 0:
        if meta_count == 0:
            return 0, match.end(2), Node(None, None)

        metas_match = re.search(
            r" (\d+)" * meta_count, input_string[match.end(2) :]
        )
        metas = [int(value) for value in metas_match.groups()]
        meta_sum = sum(metas)

        return (
            meta_sum,
            match.end(2) + metas_match.end(meta_count),
            Node(None, metas),
        )
    else:
        total_child_metas_sum = 0
        start_index = match.end(2)
        child_nodes = []

        for _ in range(child_count):
            child_metas_sum, child_end_index, child_node = process(
                input_string[start_index:]
            )
            start_index += child_end_index
            total_child_metas_sum += child_metas_sum
            child_nodes.append(child_node)

        if meta_count == 0:
            return total_child_metas_sum, start_index, Node(child_nodes, None)
        metas_match = re.search(
            r" (\d+)" * meta_count, input_string[start_index:]
        )
        metas = [int(value) for value in metas_match.groups()]
        meta_sum = sum(metas)
        return (
            meta_sum,
            start_index + metas_match.end(meta_count),
            Node(child_nodes, metas),
        )


def calc_node_value(node):
    if node.childs is None:
        node_value = sum(node.metas) if node.metas is not None else 0
        return node_value
    else:
        node_value = 0
        for meta in node.metas:
            node_index = meta - 1
            if node_index < 0 or meta > len(node.childs):
                continue
            else:
                node_value += calc_node_value(node.childs[node_index])
        return node_value


if __name__ == "__main__":
    with open("nodes.txt") as nodes_file:
        input_string = nodes_file.read().strip()
        # input_string = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
        meta_sum, _, root_node = process(input_string)
        # print(meta_sum)
        root_value = calc_node_value(root_node)
        print(root_value)
