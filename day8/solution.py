class Node:
    def __init__(self, numbers, offset = 0):
        self.child_q = numbers.pop(offset)
        self.metadata_q = numbers.pop(offset)
        self.metadata = []
        self.children = []

        if self.child_q == 0:
            for _ in range(self.metadata_q):
                self.metadata.append(numbers.pop(0))
        else:
            for _ in range(self.child_q):
                self.children.append(Node(numbers, offset))

            for _ in range(self.metadata_q):
                self.metadata.append(numbers.pop(0))
            
    def get_metadata_sum(self):
        return sum(self.metadata) + sum([node.get_metadata_sum() for node in self.children])
    
    def get_value(self):
        if not self.children:
            return sum(self.metadata)
        s = 0
        for data in self.metadata:
            if data <= len(self.children):
                s += self.children[data-1].get_value()
        return s

with open('./input.txt') as f:
    numbers = [int(x) for x in f.readline().split()]
    root = Node(numbers)
    print(root.get_metadata_sum())
    print(root.get_value())