import re

class Node:
    def __init__(self, name):
        self.nodes_before = []
        self.name = name
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

def log(nodes):
    for node in nodes:
        print('Node', node.name, ':', node.nodes_before)

with open('./input.txt') as f:
    answer = ''
    nodes = []
    for line in f.readlines():
        node_first, node_after = [*map(Node, re.search(r'Step (\w) .* step (\w)', line).groups())]
        if node_first not in nodes:
            nodes.append(node_first)
        if node_after not in nodes:
            nodes.append(node_after)
        nodes[nodes.index(node_after)].add_before_node(node_first.name)
    while nodes:
        next_node = sorted([node for node in nodes if not node.nodes_before])[0]
        answer += next_node.name
        for node in nodes:
            if next_node in node.nodes_before:
                node.nodes_before.remove(next_node)
        nodes.remove(next_node)
    print(answer)