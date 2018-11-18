import math

class Graph:
	def __init__(self, nodes, edges, epsilonDistance):
		self.nodes = nodes
		self.edges = edges
		self.radius = epsilonDistance
	def __str__(self):
		return "Wierzcholki:\n" + \
		"\n".join(map(lambda x: str(x), self.nodes)) + "\n" + \
		"\nKrawedzie:\n" + \
		"\n".join(map(lambda x: str(x), self.edges))
	def isConsistent(self):
		visited = [False] * len(self.nodes)
		stack = []
		vc = 0
		stack.append(0)
		visited[0] = True
		while(len(stack) != 0):
			v = stack.pop()
			vc = vc + 1
			for neighbour in self.nodes[v].neighbours:
				if(visited[neighbour.id] == False):
					visited[neighbour.id] = True
					stack.append(neighbour.id)
		return vc == len(self.nodes)
		
class Node:
	x: int
	y: int
	id: int
	def __init__(self, x, y, id):
		self.x = x
		self.y = y
		self.id = id
		self.neighbours = []
	def addNeighbour(self, node):
		self.neighbours.append(node)
	def __str__(self):
		return "ID: " + str(self.id) + " X: " + str(self.x) + " Y: " + str(self.y)
	
class Edge:
	node1: Node
	node2: Node
	def __init__(self, node1, node2):
		self.node1 = node1
		self.node2 = node2
	def __str__(self):
		return "Nodes: (" + str(self.node1.id) + ", " + str(self.node2.id) + ")"

def distanceBetweenNodes(node1: Node, node2: Node):
	diffX = node2.x - node1.x
	diffY = node2.y - node1.y
	return math.sqrt(diffX * diffX + diffY * diffY)
	
	