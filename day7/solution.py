from copy import deepcopy
import re

class Node:
    def __init__(self, name):
        self.nodes_before = []
        self.name = name
        self.time_to_finish = 61 + ord(name) - ord('A')
    def add_before_node(self, node):
        self.nodes_before.append(node)
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            raise 'Not implemented'
    def __lt__(self, other):
        return self.name < other.name

with open('./input.txt') as f:
    answer = ''
    nodes = []
    nodes_part2 = []
    for line in f.readlines():
        node_first, node_after = [*map(Node, re.search(r'Step (\w) .* step (\w)', line).groups())]
        if node_first not in nodes:
            nodes.append(node_first)
        if node_after not in nodes:
            nodes.append(node_after)
        nodes[nodes.index(node_after)].add_before_node(node_first.name)
    nodes_part2 = sorted([deepcopy(node) for node in nodes])
    while nodes:
        next_node = sorted([node for node in nodes if not node.nodes_before])[0]
        answer += next_node.name
        for node in nodes:
            if next_node in node.nodes_before:
                node.nodes_before.remove(next_node)
        nodes.remove(next_node)
    print(answer)

    # part 2
    answer = ''
    total_time = 0
    workers = 6
    queue = []

    while nodes_part2 or queue:
        next_nodes = sorted([node for node in nodes_part2 if not node.nodes_before])
        while len(queue) < workers and next_nodes:
            next_node = next_nodes.pop(0)
            queue.append(next_node)
            nodes_part2.remove(next_node)
        min_time_to_finish = min(queue, key=lambda node: node.time_to_finish).time_to_finish or 0
        total_time += min_time_to_finish
        queue = sorted(queue)
        nodes_to_remove = []
        for node in queue:
            node.time_to_finish -= min_time_to_finish
            if node.time_to_finish <= 0:
                nodes_to_remove.append(node)
                
        for node in nodes_to_remove:
            queue.remove(node)
            answer += node.name
            for node_to_clean in nodes_part2 + queue:
                if node in node_to_clean.nodes_before:
                    node_to_clean.nodes_before.remove(node)

    print(answer)
    print(total_time)