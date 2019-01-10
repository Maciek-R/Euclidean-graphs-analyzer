from typing import List, Dict


class Results:
    comps_sizes: List[int]
    comps_sizes_mean: float
    comps_sizes_stdev: float
    consistency_prob: float

    def __init__(self,
                 comps_sizes: List[int],
                 comps_sizes_mean: float,
                 comps_sizes_stdev: float,
                 consistency_prob: float) -> None:
        self.comps_sizes = comps_sizes
        self.comps_sizes_mean = comps_sizes_mean
        self.comps_sizes_stdev = comps_sizes_stdev
        self.consistency_prob = consistency_prob


ResultsSet = Dict[str, Dict[str, Results]]
