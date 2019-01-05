import random
import math
from typing import List, Set, Dict


class Node:
    neighbours: List['Node']
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.neighbours = []

    def add_neighbour(self, node: 'Node'):
        assert node not in self.neighbours
        self.neighbours.append(node)


def nodes_distance(node1: Node, node2: Node):
    dx = node2.x - node1.x
    dy = node2.y - node1.y
    return math.sqrt(dx*dx + dy*dy)


class Graph:
    nodes: List[Node]

    def __init__(self, nodes: List[Node] = []) -> None:
        self.nodes = nodes

    def max_component_size(self) -> int:
        stack: List[Node] = []
        visited: Set[Node] = set()
        max_size = 0

        for node in self.nodes:
            if node in visited:
                continue

            size = 1
            visited.add(node)
            stack.append(node)
            while stack:
                next_node = stack.pop()
                if next_node in visited:
                    continue

                for neighbour in next_node.neighbours:
                    if neighbour in visited:
                        continue

                    size += 1
                    visited.add(neighbour)
                    stack.append(neighbour)

            if size > max_size:
                max_size = size

        return max_size

    def consistent(self) -> bool:
        return (self.max_component_size() == len(self.nodes))
