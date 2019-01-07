import logging
import os.path
import pickle
import sys
import gzip
import math
from pathlib import Path
from typing import Optional
from multiprocessing import Pool

from utils import *

GRAPHS_PER_PART = 25


class GraphDatabase:
    output_dir: str

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir

    @property
    def logger(self):
        return logging.getLogger("GraphDatabase")

    def try_read_graphs(self, size: int, radius: float,
                        count: int, pool: Pool) -> List[Graph]:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0
        assert count >= 0

        parts_count = math.ceil(count / GRAPHS_PER_PART)
        make_part_path = lambda part: self.make_path(size, radius, part)
        parts_paths = [make_part_path(part) for part in range(parts_count)]
        graphs_parts = pool.map(self.try_read_graphs_part, parts_paths)

        graphs: List[Graph] = []
        for graphs_part in graphs_parts:
            graphs += graphs_part
        return graphs

    def try_read_graphs_part(self, part_path: Path) -> List[Graph]:
        if not part_path.is_file():
            self.logger.debug("There is no graphs file: %s", part_path)
            return []

        self.logger.debug("Reading graphs file: %s...", part_path)
        with gzip.open(part_path, 'rb') as ifile:
            try:
                return pickle.load(ifile)
            except:
                self.logger.error("Could not read graphs file: %s!", part_path)
                return []

    def write_graphs(self, size: int, radius: float,
                     graphs: List[Graph], pool: Pool) -> None:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0

        k = GRAPHS_PER_PART
        graphs_parts = [graphs[i:i+k] for i in range(0, len(graphs), k)]
        make_part_path = lambda part: self.make_path(size, radius, part)
        parts_paths = [make_part_path(part) for part in range(len(graphs_parts))]
        args = [(graphs_parts[i], parts_paths[i]) for i in range(len(graphs_parts))]
        pool.starmap(self.write_graphs_part, args)

    def write_graphs_part(self, graphs: List[Graph], path: Path) -> None:
        self.logger.debug("Writing graphs to file: %s...", path)
        with gzip.open(path, 'wb') as ofile:
            pickle.dump(graphs, ofile)

    def make_path(self, size: int, radius: float, part: int) -> Path:
        assert size > 0
        assert radius >= 0.0 and radius <= 1.0

        # Resulted path will be like: '<size>-<radius>(<part>).graph.gz'
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        return Path('{}/{}-{}({}).graphs.gz'.format(self.output_dir,
                                                    size_str,
                                                    radius_str,
                                                    part))
