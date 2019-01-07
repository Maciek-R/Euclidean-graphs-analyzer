import math
import logging
import json
from pathlib import Path
from typing import Optional, Sequence
from multiprocessing import Pool

from common import *
from graph_gen import GraphGenerator

ComponentsSizesSet = Dict[int, Dict[float, List[int]]]


class GraphAnalyzer:
    output_dir: str
    generator: GraphGenerator
    log: logging.Logger

    def __init__(self, output_dir: str, generator: GraphGenerator) -> None:
        self.output_dir = output_dir
        self.generator = generator
        self.log = logging.getLogger("GraphAnalyzer")

    def __call__(self, sizes: Sequence[int],
                 radiuses: Sequence[float],
                 count: int,
                 pool: Pool) -> ComponentsSizesSet:
        assert count >= 0
        self.log.debug("Performing analysis...")

        comps_sizes_set = self.load_max_comps_sizes()
        try:
            for size in sizes:
                assert size > 0
                if size not in comps_sizes_set:
                    comps_sizes_set[size] = {}
                comps_sizes_subset = comps_sizes_set[size]

                for radius in radiuses:
                    assert radius >= 0.0 and radius <= 1.0
                    if radius not in comps_sizes_subset:
                        comps_sizes_subset[radius] = []
                    comps_sizes = comps_sizes_subset[radius]

                    graphs = self.generator(size, radius, count, pool)
                    if len(graphs) > len(comps_sizes):
                        idx_from, idx_to = len(comps_sizes), len(graphs)
                        self.log.debug("Calculating max components sizes for"
                                       " graphs n: %s, r: %s, #: %s-%s...",
                                       size, radius, idx_from, idx_to)
                        comps_sizes += pool.map(Graph.max_component_size,
                                                graphs[idx_from:idx_to])
        finally:
            self.save_max_comps_sizes(comps_sizes_set)

        return comps_sizes_set

    def load_max_comps_sizes(self) -> ComponentsSizesSet:
        path = Path(self.output_dir + "/max_comps_size.json")
        if not path.is_file():
            self.log.warn("There is no maximal components sizes cache file")
            return {}

        self.log.debug("Loading cached maximal components sizes from file...")
        with open(path, "r") as ifile:
            return json.load(ifile)

    def save_max_comps_sizes(self,
                             comps_sizes_set: ComponentsSizesSet) -> None:
        self.log.debug("Saving maximal components size to file...")
        path = Path(self.output_dir + "/max_comps_size.json")
        with open(path, "w") as ofile:
            return json.dump(comps_sizes_set, ofile)
