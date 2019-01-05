import random
import math
from typing import List, Set, Dict


class Node:
    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y


def nodes_distance_sq(node1: Node, node2: Node):
    dx = node2.x - node1.x
    dy = node2.y - node1.y
    return (dx*dx + dy*dy)


class Graph:
    nodes: List[Node]
    edges: List[List[bool]]

    def __init__(self, size: int) -> None:
        assert size >= 0

        self.nodes = [Node()] * size
        self.edges = [[False] * size] * size

    def max_component_size(self) -> int:
        stack: List[int] = []
        visited: List[bool] = [False] * len(self.nodes)
        max_size = 0

        for u in range(len(self.nodes)):
            if visited[u]:
                continue

            size = 1
            visited[u] = True
            stack.append(u)
            while stack:
                v = stack.pop()
                v_edges = self.edges[v]

                for k in range(len(self.nodes)):
                    if visited[k]:
                        continue

                    if not v_edges[k]:  # Not a neighbour
                        continue

                    size += 1
                    visited[k] = True
                    stack.append(k)

            if size > max_size:
                max_size = size

        return max_size

    def consistent(self) -> bool:
        return (self.max_component_size() == len(self.nodes))
