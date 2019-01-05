import random
import math
import logging
import os.path
import pickle
import sys
import gzip
from pathlib import Path
from typing import Sequence, TypeVar, Dict, Optional

from utils import *


class GraphGenerator:
    output_dir: str
    log: logging.Logger

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self.log = logging.getLogger("GraphFactory")

        # Set recursion limit for read-write operations on graphs
        sys.setrecursionlimit(50000)

    def __call__(self, size: int,
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

        path = self.make_path(size, radius, index)
        graph = self.read_graph(path)
        if graph is None:
            self.log.debug("Generating graph n=%s, r=%s (#%s)",
                           size, radius, index)
            graph = self.random_euclidean_graph(size, radius)

        if not path.is_file():
            self.write_graph(graph, path)

        assert graph is not None
        return graph

    def make_path(self, size: int, radius: float, index: int) -> Path:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        # Resulted path will be like: '<size>-<radius>(index).graph'
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        index_str = str(index)
        return Path('{}/{}-{}({}).graph'.format(self.output_dir,
                                                size_str,
                                                radius_str,
                                                index_str))

    def read_graph(self, path: Path) -> Optional[Graph]:
        if not path.is_file():
            return None

        final_path = str(path) + ".gz"
        self.log.debug("Reading graph file: %s...", final_path)
        with gzip.open(final_path, 'rb') as ifile:
            try:
                graph = pickle.load(ifile)
                return graph
            except pickle.UnpicklingError:
                self.log.error("Could not read graph file: %s!", final_path)
                return None

    def write_graph(self, graph: Graph, path: Path) -> None:
        final_path = str(path) + ".gz"
        self.log.debug("Writing graph to file: %s...", final_path)
        with gzip.open(final_path, 'wb') as ofile:
            pickle.dump(graph, ofile)

    def random_euclidean_graph(self, size: int = 10,
                               radius: float = 0.5) -> Graph:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0

        self.log.debug("Generating nodes...")
        nodes: List[Node] = []
        for i in range(size):
            x = round(random.random(), ndigits=5)
            y = round(random.random(), ndigits=5)
            nodes.append(Node(x, y))

        self.log.debug("Connecting adjacents...")
        for i in range(len(nodes)):
            node1 = nodes[i]
            for node2 in nodes[i+1:]:
                distance = nodes_distance(node1, node2)
                if(distance <= radius):
                    node1.add_neighbour(node2)
                    node2.add_neighbour(node1)

        return Graph(nodes)
