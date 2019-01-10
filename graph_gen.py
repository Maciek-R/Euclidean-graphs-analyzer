"""Contains implementation of GraphGenerator class
Provides functionality of generating Graph instances. At the moment, it could
generate only random euclidean graphs.
"""
import random
import math
import logging
from typing import Sequence

from utils import *
from graph_db import GraphDatabase


def random_euclidean_graph(size: int, radius: float) -> Graph:
    """Generates random euclidean graph of given size and radius
    Euclidean graph is a graph in which nodes are placed in a unit square
    [0.0; 1.0] x [0.0; 1.0]. Connection between nodes depends on its euclidean
    distance. If it is less or equal than given radius, they become neighbours.

    Operation is done in three stages:
        1. Creating graph of given size (n)
        2. Generating nodes positions (complexity O(n))
        3. Connecting adjacent nodes - euclidean distance between them are
            less than or equal to given radius (complexity O(n^2))

    To improve performance, it uses square of euclidean distance
    (see `nodes_distance_sq`) to avoid unnecessary calculations of square root
    in every iteration.

    Args:
        size (int): size of graph, must be greater than zero
        radius (float): radius of graph, must be in range [0.0; 1.0]

    Returns:
        Graph: random euclidean graph of given size and radius
    """
    assert size >= 0
    assert radius >= 0.0 and radius <= 1.0
    graph = Graph(size)

    # Generate nodes positions
    for node in graph.nodes:
        node.x = random.random()
        node.y = random.random()

    # Connect adjacents
    radius_sq = (radius ** 2)
    for u in range(len(graph.nodes)):
        u_node = graph.nodes[u]
        u_edges = graph.edges[u]

        for v in range(len(graph.nodes))[u+1:]:
            v_node = graph.nodes[v]
            v_edges = graph.edges[v]

            distance_sq = nodes_distance_sq(u_node, v_node)
            if(distance_sq <= radius_sq):
                u_edges[v] = True
                v_edges[u] = True

    return graph


class GraphGenerator:

    """Generates random euclidean graphs
    It uses internally `GraphDatabase` class to store generated graphs (and to
    just read them, when needed).

    Attributes:
        db (GraphDatabase): database of graphs
    """

    db: GraphDatabase

    def __init__(self, db: GraphDatabase) -> None:
        """Constructor
        Initializes attributes

        Args:
            db (GraphDatabase): database of graphs
        """
        self.db = db

    @property
    def logger(self) -> logging.Logger:
        """Returns class logger instance

        Returns:
            logging.Logger: Returns class logger instance
        """
        return logging.getLogger("GraphGenerator")

    def __call__(self, size: int,
                 radius: float,
                 index: int) -> Graph:
        """Generates random euclidean graph of given size, radius, index
        It first tries to load graph from the GraphDatabase. If there is one
        arleady, it will be returned. In other case, graph will be generated
        using `random_euclidean_graph` method and stored then to database

        Args:
            size (int): size of graph, must be greater than zero
            radius (float): radius of graph, must be in range [0.0; 1.0]
            index (int): index of graph, must be non-negative

        Returns:
            Graph: Description
        """
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        graph = self.db.try_read_graph(size, radius, index)
        if graph is None:
            self.logger.debug("Generating graph, n=%s, r=%s (#%s)...",
                              size, radius, index)
            graph = random_euclidean_graph(size, radius)
            self.db.write_graph(size, radius, index, graph)

        return graph
