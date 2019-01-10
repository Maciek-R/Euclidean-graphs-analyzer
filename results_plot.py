import csv
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional


class ResultsPlotter(ABC):
    @abstractmethod
    def plot(self, results_set) -> None:
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

    def plot(self, results_set) -> None:
        self.logger.debug("Plotting results...")
        for size, results_subset in results_set.items():
            for radius, comps_sizes in results_subset.items():
                path = self.make_path(size, radius)
                self.logger.debug("Plotting to %s...", path)
                with open(path, 'w') as csvfile:
                    fieldnames = ['index', 'max_comp_size']
                    writer = csv.DictWriter(csvfile,
                                            delimiter=self.delimiter,
                                            fieldnames=fieldnames)
                    rows = [{'index': index,
                             'max_comp_size': max_comp_size}
                            for index, max_comp_size in enumerate(comps_sizes)]
                    writer.writeheader()
                    writer.writerows(rows)

    def make_path(self, size, radius) -> Path:
        size_str = str(size)
        radius_str = str(radius).replace('.', '_')
        fname_fmt = '{}-{}-max_comps_sizes.csv'
        fname = Path(fname_fmt.format(size_str, radius_str))
        return Path.joinpath(self.output_dir, fname)


class PNGResultsPlotter(ResultsPlotter):
    output_dir: Path

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def plot(self, results_set) -> None:
        raise NotImplementedError()


class NullResultsPlotter(ResultsPlotter):
    def plot(self, results_set) -> None:
        pass


def plotter(plot_type: Optional[str], output_dir: Path):
    if plot_type == "CSV":
        return CSVResultsPlotter(output_dir)
    elif plot_type is None:
        return NullResultsPlotter()
    else:
        raise ValueError("Invalid plot_type: " + str(plot_type))
