import random
import math
import logging
from typing import Sequence

from common import *
from graph_loader import GraphLoader


class GraphGenerator:
    loader: GraphLoader
    log: logging.Logger

    def __init__(self, loader: GraphLoader) -> None:
        self.loader = loader
        self.log = logging.getLogger("GraphGenerator")

    def __call__(self, sizes: Sequence[int],
                 radiuses: Sequence[float],
                 repeats: int) -> GraphsSet:
        assert repeats >= 0
        self.log.info("Generating total %s graphs...",
                      len(sizes)*len(radiuses)*repeats)

        graphs_set: GraphsSet = {}
        for size in sizes:
            graphs_subset = graphs_set[size] = {}
            for radius in radiuses:
                graphs = self.generate_graphs(size, radius, repeats)
                graphs_subset[radius] = graphs

        return graphs_set

    def generate_graphs(self, size: int,
                        radius: float,
                        count: int = 1) -> List[Graph]:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert count > 0

        graphs: List[Graph] = []
        self.log.debug("Generating %s graphs of size: %s, radius: %s...",
                       count, size, radius)

        for index in range(count):
            graphs.append(self.generate_one(size, radius, index))

        return graphs

    def generate_one(self, size: int,
                     radius: float,
                     index: int) -> Graph:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        # Retrieve or (if not present/or corrupted) generate a new graph
        graph = self.loader.try_read_graph(size, radius, index)
        if graph is None:
            self.log.debug("Generating graph n=%s, r=%s (#%s)...",
                           size, radius, index)
            graph = self.random_euclidean_graph(size, radius)

        self.loader.write_graph(size, radius, index, graph)
        return graph

    def random_euclidean_graph(self, size: int = 10,
                               radius: float = 0.5) -> Graph:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0

        graph = Graph(size)
        self.generate_graph_positions(graph)
        self.connect_graph_adjacents(graph, radius)
        return graph

    def generate_graph_positions(self, graph: Graph) -> None:
        self.log.debug("Generating positions...")
        for node in graph.nodes:
            node.x = round(random.random(), ndigits=5)
            node.y = round(random.random(), ndigits=5)

    def connect_graph_adjacents(self, graph: Graph, radius: float) -> None:
        assert radius >= 0.0 and radius <= 1.0
        self.log.debug("Connecting adjacents...")

        radius_sq = radius*radius
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
