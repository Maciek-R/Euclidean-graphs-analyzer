"""Algorithms and structures used in graphs analysis
Contains implementation of classes like `Node`, `Graph` and helper functions
 like `nodes_distance_sq` or `max_component_size`
"""
from typing import List, Dict


class Node:

    """Represents a node in graph

    Attributes:
        x (float): position
        y (float): position
    """

    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """Constructor
        Initializes nodes attributes

        Args:
            x (float, optional): position
            y (float, optional): position
        """
        self.x = x
        self.y = y


def nodes_distance_sq(node1: Node, node2: Node):
    """Calculates square of euclidean distance between two nodes

    Args:
        node1 (Node):
        node2 (Node):

    Returns:
        TYPE: square of euclidean distance between nodes
    """
    dx = node2.x - node1.x
    dy = node2.y - node1.y
    return (dx*dx + dy*dy)


class Graph:

    """Represents graphs using array of nodes and boolean adjacency matrix
    Its functionality is maximally reduced to gain maximum perfomance
    and low memory usage. It is intended only to create graph
    of specified size. There is no way to resize graph or
    append/remove nodes to/from it. The only method available for user is
    `max_component_size`, which calculates size of the maximum component.

    Nodes are stored in single array. This way, index of node in array is at
    the same time its unique identifier, which is used in adjacency matrix.

    Adjacencies between nodes are stored using `edges` attribute. It is
    a binary matrix of size N x N, where N is graph size. If there is
    a connection between nodes, say on indices `v` and `u`, corresponding cell
    in matrix should be marked as `True`. It is up to caller to initialize
    `edges` attribute with correct values. The user decides, whether graph
    should be directed or not.

    Attributes:
        edges (List[bytearray]): Boolean adjacency matrix
        nodes (List[Node]): Nodes array
    """

    edges: List[bytearray]
    nodes: List[Node]

    def __init__(self, size: int) -> None:
        """Constructor
        Creates array of default initialized nodes (`size` elements)
        and initializes adjacency matrix to have False values
        (`size` on `size` elements).

        Args:
            size (int): Size of graph. Should be greater than zero
        """
        assert size >= 0

        self.nodes = [Node() for _ in range(size)]
        self.edges = [bytearray(size) for _ in range(size)]

    def max_component_size(self) -> int:
        """Calculates size of the maximum component in graph
        Since graph implementation is based on continuous range of nodes
        (they have identifiers/indices from 0 to N), it uses stack
        of integers (nodes indices) to implement DFS algorithm
        (Depth First Search). It uses also N-element boolean array to mark,
        whether particular node was visited or not.
        During each DFS process it calculates size of component and at the end
        returns the largest one. If the result is equal to the size of
        graph (number of nodes) it means, that graph is consistent.

        Returns:
            int: size of the maximum component in graph
        """
        nodes_len = len(self.nodes)
        stack: List[int] = []
        visited = [False]*nodes_len
        max_size = 0

        for u in range(nodes_len):
            if visited[u]:
                continue

            size = 1
            visited[u] = True
            stack.append(u)
            while stack:
                v = stack.pop()
                v_edges = self.edges[v]

                for k in range(nodes_len):
                    if not v_edges[k]:  # Not a neighbour
                        continue
                    if visited[k]:
                        continue

                    size += 1
                    visited[k] = True
                    stack.append(k)

            if size > max_size:
                max_size = size

        return max_size
