from argparse import ArgumentParser, ArgumentTypeError, Action
import logging
import numpy as np
import sys

from graph_test import GraphTester
from graph_gen import GraphGenerator


class SizeAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0:
            parser.error("Size should be greater than zero")

        setattr(namespace, self.dest, values)


class RadiusAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0.0 or values > 1.0:
            parser.error("Radius should be in range [0.0; 1.0]")

        setattr(namespace, self.dest, values)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Euclidean graphs test suite")

    parser.add_argument("--start_size",
                        action=SizeAction,
                        type=int,
                        metavar="SIZE",
                        required=True,
                        help="Size of the first graph")
    parser.add_argument("--stop_size",
                        action=SizeAction,
                        type=int,
                        metavar="SIZE",
                        required=True,
                        help="Size of the last graph")
    parser.add_argument("--size_step",
                        action="store",
                        type=int,
                        metavar="STEP",
                        default=1,
                        help="Step between graphs sizes. Default: 1")

    parser.add_argument("--start_radius",
                        action=RadiusAction,
                        type=float,
                        metavar="RADIUS",
                        required=True,
                        help="Radius of the first graph")
    parser.add_argument("--stop_radius",
                        action=RadiusAction,
                        type=float,
                        metavar="RADIUS",
                        required=True,
                        help="Radius of the last graph")
    parser.add_argument("--radius_step",
                        action="store",
                        type=float,
                        metavar="STEP",
                        default=0.01,
                        help="Step between graphs radiuses: Default: 0.01")

    parser.add_argument("--repeats", "-r",
                        action="store",
                        type=int,
                        metavar="COUNT",
                        default=1,
                        help="How many repeat tests for each graph type")
    parser.add_argument("--output_dir", "-o",
                        action="store",
                        type=str,
                        metavar="DIR",
                        default="output/",
                        help="Directory for output files: Default: 'output/'")
    parser.add_argument("--verbose", "-v",
                        action="store_true",
                        help="Displays more messages")

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    logging.info("Initializing...")

    generator = GraphGenerator(args.output_dir)
    tester = GraphTester(generator)

    sizes = range(args.start_size,
                  args.stop_size + 1,
                  args.size_step)
    radiuses = np.arange(args.start_radius,
                         args.stop_radius + sys.float_info.epsilon,
                         args.radius_step)

    logging.info("Running test...")
    tester.run(sizes, radiuses, args.repeats)
    logging.info("Finished")
