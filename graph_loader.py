import logging
import os.path
import pickle
import sys
import gzip
from pathlib import Path
from typing import Optional

from utils import *


class GraphLoader:
    output_dir: str
    log: logging.Logger

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self.log = logging.getLogger("GraphLoader")

    def try_read_graph(self, size: int, radius: float,
                       index: int) -> Optional[Graph]:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        path = self.make_path(size, radius, index)
        if not path.is_file():
            self.log.debug("There is no graph file: %s", path)
            return None

        self.log.debug("Reading graph file: %s...", path)
        with gzip.open(path, 'rb') as ifile:
            try:
                graph = pickle.load(ifile)
                return graph
            except pickle.UnpicklingError:
                self.log.error("Could not read graph file: %s!", path)
                return None

    def write_graph(self, size: int, radius: float, index: int,
                    graph: Graph) -> None:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        path = self.make_path(size, radius, index)
        if not path.is_file():
            self.log.debug("Writing graph to file: %s...", path)
            with gzip.open(path, 'wb') as ofile:
                pickle.dump(graph, ofile)

    def make_path(self, size: int, radius: float, index: int) -> Path:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        # Resulted path will be like: '<size>-<radius>(index).graph'
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        index_str = str(index)
        return Path('{}/{}-{}({}).graph.gz'.format(self.output_dir,
                                                   size_str,
                                                   radius_str,
                                                   index_str))
