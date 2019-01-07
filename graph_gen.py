import random
import math
import logging
from typing import Sequence
from multiprocessing import Pool

from common import *
from graph_db import GraphDatabase


def random_euclidean_graph(size: int, radius: float) -> Graph:
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
    db: GraphDatabase
    log: logging.Logger

    def __init__(self, db: GraphDatabase) -> None:
        self.db = db
        self.log = logging.getLogger("GraphGenerator")

    def __call__(self, size: int,
                 radius: float,
                 count: int,
                 pool: Pool) -> List[Graph]:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert count > 0

        graphs = self.db.try_read_graphs(size, radius, count, pool)
        diff = (count - len(graphs))
        if diff > 0:
            self.log.debug("Generating %s graphs of size: %s, radius: %s...",
                           diff, size, radius)
            graphs += pool.starmap(random_euclidean_graph,
                                   [(size, radius)] * diff)
            self.db.write_graphs(size, radius, graphs, pool)

        return graphs
