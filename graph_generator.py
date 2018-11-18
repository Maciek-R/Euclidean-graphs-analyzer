import random
import math
from utils import *

def generateGraph(numberOfNodes = 10, epsilonDistance = 0.5):
	nodes = []
	for id in range(numberOfNodes):
		x = round(random.random(), 5)
		y = round(random.random(), 5)
		nodes.append(Node(x, y, id))
	
	edges = []
	for i in range(len(nodes)):
		node1 = nodes[i]
		for node2 in nodes[i+1:]:
			distance = distanceBetweenNodes(node1, node2)
			if(distance <= epsilonDistance):
				edges.append(Edge(node1, node2))
				node1.addNeighbour(node2)
				node2.addNeighbour(node1)
				
	return Graph(nodes, edges, epsilonDistance)