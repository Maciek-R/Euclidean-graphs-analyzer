from typing import Sequence, TypeVar, Dict
import logging

from utils import *
from graph_gen import GraphGenerator

GraphsSet = Dict[int, Dict[float, List[Graph]]]
ComponentsSizesSet = Dict[int, Dict[float, List[int]]]


class GraphTester:
    output_dir: str
    graph_generator: GraphGenerator
    log: logging.Logger

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self.graph_generator = GraphGenerator(output_dir)
        self.log = logging.getLogger("GraphTester")

        self.log.debug("Initialized")

    def run(self, sizes: Sequence[int],
            radiuses: Sequence[float],
            repeats: int = 1) -> None:
        assert repeats >= 0
        self.log.info("Running graphs tests:"
                      " sizes from %s to %s (total %s),"
                      " radiuses from %s to %s (total %s)"
                      " every repeated %s times",
                      sizes[0], sizes[-1], len(sizes),
                      radiuses[0], radiuses[-1], len(radiuses),
                      repeats)

        graphs = self.generate_graphs(sizes, radiuses, repeats)
        comps_sizes = self.max_components_sizes(graphs)

    def generate_graphs(self, sizes: Sequence[int],
                        radiuses: Sequence[float],
                        repeats: int) -> GraphsSet:
        assert repeats >= 0
        self.log.info("Generating total %s graphs...",
                      len(sizes)*len(radiuses)*repeats)

        graphs_set: GraphsSet = {}
        for size in sizes:
            graphs_subset = graphs_set[size] = {}
            for radius in radiuses:
                graphs = self.graph_generator(size, radius, count=repeats)
                graphs_subset[radius] = graphs

        return graphs_set

    def max_components_sizes(self,
                             graphs_set: GraphsSet) -> ComponentsSizesSet:
        self.log.info("Calculating maximal components sizes...")
        comps_sizes_set: ComponentsSizesSet = {}
        for size, graph_subset in graphs_set.items():
            comps_sizes_subset = comps_sizes_set[size] = {}
            for radius, graphs in graph_subset.items():
                self.log.debug("Calculating max components sizes for graphs"
                               " n: %s, r: %s", size, radius)
                comps_sizes = [g.max_component_size() for g in graphs]
                comps_sizes_subset[radius] = comps_sizes

        return comps_sizes_set
