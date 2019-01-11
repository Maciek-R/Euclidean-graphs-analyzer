import csv
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional

from common import *


class ResultsPlotter(ABC):
    @abstractmethod
    def plot(self, results_set: ResultsSet) -> None:
        pass


class CSVResultsPlotter(ResultsPlotter):
    output_dir: Path
    delimiter: str

    def __init__(self, output_dir: Path, delimiter: str = ' ') -> None:
        assert output_dir.is_dir()
        self.output_dir = output_dir
        self.delimiter = delimiter
        self.logger.debug("Initialized")

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger("CSVResultsPlotter")

    def plot(self, results_set: ResultsSet) -> None:
        self.logger.debug("Plotting results...")
        self.plot_comps_sizes(results_set)
        self.plot_others(results_set)

    def plot_comps_sizes(self, results_set: ResultsSet) -> None:
        self.logger.debug("Plotting max comps sizes...")
        for size, results_subset in results_set.items():
            size_n = int(size)
            for radius, results in results_subset.items():
                radius_f = float(radius)
                path = self.make_path_max_comps_sizes(size_n, radius_f)
                self.logger.debug("Plotting to %s...", path)

                with open(path, 'w') as csvfile:
                    fieldnames = ['index', 'max_comp_size']
                    writer = csv.DictWriter(csvfile,
                                            delimiter=self.delimiter,
                                            fieldnames=fieldnames)

                    comps_sizes = results.comps_sizes
                    rows = [{'index': index,
                             'max_comp_size': max_comp_size}
                            for index, max_comp_size in enumerate(comps_sizes)]
                    writer.writeheader()
                    writer.writerows(rows)

    def plot_others(self, results_set: ResultsSet) -> None:
        self.logger.debug("Plotting others...")
        for size, results_subset in results_set.items():

            radiuses = sorted(results_subset.keys())[-1]
            radius_from = float(radiuses[0])
            radius_to = float(radiuses[-1])

            path = self.make_path_max_comps_sizes_means_r(int(size),
                                                          radius_from,
                                                          radius_to)
            self.logger.debug("Plotting to %s...", path)
            with open(path, 'w') as csvfile:
                fieldnames = ['radius', 'comps_sizes_mean']
                writer = csv.DictWriter(csvfile,
                                        delimiter=self.delimiter,
                                        fieldnames=fieldnames)

                rows = [{'radius': radius,
                         'comps_sizes_mean': results.comps_sizes_mean}
                        for radius, results in results_subset.items()]
                writer.writeheader()
                writer.writerows(rows)

            path = self.make_path_consistency_prob_r(int(size),
                                                     radius_from,
                                                     radius_to)
            self.logger.debug("Plotting to %s...", path)
            with open(path, 'w') as csvfile:
                fieldnames = ['radius', 'consistency_prob']
                writer = csv.DictWriter(csvfile,
                                        delimiter=self.delimiter,
                                        fieldnames=fieldnames)

                rows = [{'radius': radius,
                         'consistency_prob': results.consistency_prob}
                        for radius, results in results_subset.items()]
                writer.writeheader()
                writer.writerows(rows)

    def make_path_max_comps_sizes(self, size: int, radius: float) -> Path:
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        fname_fmt = '{}-{}-max_comps_sizes.csv'
        fname = Path(fname_fmt.format(size_str, radius_str))
        return Path.joinpath(self.output_dir, fname)

    def make_path_max_comps_sizes_means_r(self, size: int,
                                          radius_from: float,
                                          radius_to: float) -> Path:
        size_str = str(size)
        radius_from_str = str(radius_from).replace('.', '_')
        radius_to_str = str(radius_to).replace('.', '_')
        fname_fmt = '{}-{}:{}-max_comps_sizes_means.csv'
        fname = Path(fname_fmt.format(size_str,
                                      radius_from_str,
                                      radius_to_str))
        return Path.joinpath(self.output_dir, fname)

    def make_path_consistency_prob_r(self, size: int,
                                     radius_from: float,
                                     radius_to: float) -> Path:
        size_str = str(size)
        radius_from_str = str(radius_from).replace('.', '_')
        radius_to_str = str(radius_to).replace('.', '_')
        fname_fmt = '{}-{}:{}-consistency_prob.csv'
        fname = Path(fname_fmt.format(size_str,
                                      radius_from_str,
                                      radius_to_str))
        return Path.joinpath(self.output_dir, fname)


class NullResultsPlotter(ResultsPlotter):
    def plot(self, results_set: ResultsSet) -> None:
        pass


def plotter(plot_type: Optional[str], output_dir: Path):
    if plot_type == "CSV":
        return CSVResultsPlotter(output_dir)
    elif plot_type is None:
        return NullResultsPlotter()
    else:
        raise ValueError("Invalid plot_type: " + str(plot_type))
