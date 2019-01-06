from typing import Sequence, Dict, Optional
from multiprocessing import Pool
import logging

from common import *
from graph_gen import GraphGenerator
from graph_analyze import GraphAnalyzer


class GraphTester:
    graph_generator: GraphGenerator
    graph_analyzer: GraphAnalyzer
    log: logging.Logger

    def __init__(self, graph_generator: GraphGenerator,
                 graph_analyzer: GraphAnalyzer) -> None:
        self.graph_generator = graph_generator
        self.graph_analyzer = graph_analyzer
        self.log = logging.getLogger("GraphTester")

        self.log.debug("Initialized")

    def run(self, sizes: Sequence[int],
            radiuses: Sequence[float],
            repeats: int = 1,
            pool: Optional[Pool] = None) -> None:
        assert repeats >= 0
        self.log.info("Running graphs tests:"
                      " sizes from %s to %s (total %s),"
                      " radiuses from %s to %s (total %s)"
                      " every repeated %s times",
                      sizes[0], sizes[-1], len(sizes),
                      radiuses[0], radiuses[-1], len(radiuses),
                      repeats)

        graphs_set = self.graph_generator(sizes, radiuses, repeats)
        comps_sizes_set = self.graph_analyzer(graphs_set, pool)
