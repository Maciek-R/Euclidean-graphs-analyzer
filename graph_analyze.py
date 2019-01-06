import math
import logging
from typing import Optional
from multiprocessing import Pool

from common import *

ComponentsSizesSet = Dict[int, Dict[float, List[int]]]


class GraphAnalyzer:
    output_dir: str
    log: logging.Logger

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self.log = logging.getLogger("GraphAnalyzer")

    def __call__(self, graphs_set: GraphsSet,
                pool: Optional[Pool] = None) -> ComponentsSizesSet:
        self.log.info("Calculating maximal components sizes...")

        comps_sizes_set: ComponentsSizesSet = {}
        for size, graph_subset in graphs_set.items():
            comps_sizes_subset = comps_sizes_set[size] = {}
            for radius, graphs in graph_subset.items():
                self.log.debug("Calculating max components sizes for graphs"
                               " n: %s, r: %s", size, radius)

                comps_sizes = self.graphs_max_comps_sizes(graphs, pool)
                comps_sizes_subset[radius] = comps_sizes

        return comps_sizes_set

    def graphs_max_comps_sizes(self,
                               graphs: List[Graph],
                               pool: Optional[Pool]) -> List[int]:
        if pool is not None:
            return pool.map(Graph.max_component_size, graphs)
        else:
            return [g.max_component_size() for g in graphs]
