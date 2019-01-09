import math
import logging
import json
from pathlib import Path
from typing import Optional, Sequence
from multiprocessing import Pool

from common import *
from graph_gen import GraphGenerator

ComponentsSizesSet = Dict[str, Dict[str, List[int]]]


class GraphAnalyzer:
    output_dir: str
    generator: GraphGenerator

    def __init__(self, output_dir: str, generator: GraphGenerator) -> None:
        self.output_dir = output_dir
        self.generator = generator

    @property
    def logger(self):
        return logging.getLogger("GraphAnalyzer")

    def __call__(self, sizes: Sequence[int],
                 radiuses: Sequence[float],
                 count: int,
                 pool: Pool) -> ComponentsSizesSet:
        assert count >= 0

        self.logger.debug("Performing analysis...")
        comps_sizes_set = self.load_max_comps_sizes()
        try:
            for size in sizes:
                assert size > 0
                size_str = str(size)
                if size_str not in comps_sizes_set:
                    comps_sizes_set[size_str] = {}
                comps_sizes_subset = comps_sizes_set[size_str]

                for radius in radiuses:
                    assert radius >= 0.0 and radius <= 1.0
                    radius_str = str(radius)
                    if radius_str not in comps_sizes_subset:
                        comps_sizes_subset[radius_str] = []
                    comps_sizes = comps_sizes_subset[radius_str]

                    if len(comps_sizes) > count:
                        # We arleady have this results
                        continue

                    indexes = range(len(comps_sizes), count)
                    args = [(size, radius, index) for index in indexes]
                    comps_sizes += pool.starmap(self.max_comp_size, args)

        finally:
            self.save_max_comps_sizes(comps_sizes_set)

        return comps_sizes_set

    def max_comp_size(self, size: int, radius: float, index: int) -> int:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        graph = self.generator(size, radius, index)
        self.logger.debug("Calculating maximal component size for "
                          " graph n=%s, r=%s (#%s)...", size, radius, index)
        return graph.max_component_size()

    def load_max_comps_sizes(self) -> ComponentsSizesSet:
        path = Path(self.output_dir + "/max_comps_size.json")
        if not path.is_file():
            self.logger.warn("There is no cached results file")
            return {}

        self.logger.debug("Loading cached results from file...")
        with open(path, "r") as ifile:
            return json.load(ifile)

    def save_max_comps_sizes(self,
                             comps_sizes_set: ComponentsSizesSet) -> None:
        self.logger.debug("Saving results to file...")
        path = Path(self.output_dir + "/max_comps_size.json")
        with open(path, "w") as ofile:
            return json.dump(comps_sizes_set, ofile)
