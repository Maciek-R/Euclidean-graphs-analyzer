import logging
import os.path
import pickle
import sys
import gzip
import math
from pathlib import Path
from typing import Optional

from utils import *


class GraphDatabase:
    output_dir: str

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir

    @property
    def logger(self):
        return logging.getLogger("GraphDatabase")

    def try_read_graph(self, size: int, radius: float,
                       index: int) -> Optional[Graph]:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        path = self.make_path(size, radius, index)
        if not path.is_file():
            self.logger.debug("There is no graph file: %s", path)
            return None

        self.logger.debug("Reading graph file: %s...", path)
        with gzip.open(path, 'rb') as ifile:
            try:
                return pickle.load(ifile)
            except:
                self.logger.error("Could not read graph file: %s!", path)
                return None

    def write_graph(self, size: int, radius: float, index: int,
                    graph: Graph) -> None:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        path = self.make_path(size, radius, index)
        self.logger.debug("Writing graph to file: %s...", path)
        with gzip.open(path, 'wb') as ofile:
            pickle.dump(graph, ofile)

    def make_path(self, size: int, radius: float, index: int) -> Path:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert index >= 0

        # Resulted path will be like: '<size>-<radius>(<index>).graph.gz'
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        return Path('{}/{}-{}({}).graph.gz'.format(self.output_dir,
                                                   size_str,
                                                   radius_str,
                                                   index))
