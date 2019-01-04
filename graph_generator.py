import random
import math
from typing import List

from utils import *


def random_euclidean_graph(size: int = 10, radius: float = 0.5) -> Graph:
    # Generate nodes placed randomly in [0.0; 1.0] x [0.0; 1.0] square
    nodes: List[Node] = []
    for i in range(size):
        x = round(random.random(), ndigits=5)
        y = round(random.random(), ndigits=5)
        nodes.append(Node(x, y))

    # Connect those nodes, which distance is less than or equal to radius
    for i in range(len(nodes)):
        node1 = nodes[i]
        for node2 in nodes[i+1:]:
            distance = nodes_distance(node1, node2)
            if(distance <= radius):
                node1.add_neighbour(node2)
                node2.add_neighbour(node1)

    return Graph(nodes)
