import csv
from utils import *
import os

mainFolder = 'data/'

def createFileNameForGraph(numberOfNodes, radius):
	if not os.path.exists(mainFolder):
		os.makedirs(mainFolder)
	return mainFolder + str(numberOfNodes) + '_' + str(radius) + '.csv'
	
def writeGraphToFile(graph):
	data = []
	data.append([str(len(graph.nodes))])
	data.append([str(graph.radius)])
	nodes = list(map(lambda node: [str(node.id) + ' ' + str(node.x) + ' ' + str(node.y)] , graph.nodes))
	edges = list(map(lambda x: [str(x.node1.id) + ' ' + str(x.node2.id)] , graph.edges))
	data = data + nodes + edges
	
	fileName = createFileNameForGraph(len(graph.nodes), graph.radius)
	file = open(fileName, 'w', newline = '\n')
	with file:
		writer = csv.writer(file)
		writer.writerows(data)
		
def readGraphFromFile(numberOfNodes, radius):
	fileName = createFileNameForGraph(numberOfNodes, radius)
	data=[]
	with open(fileName, newline='') as file:
		reader = csv.reader(file)
		for row in reader:
			data.append(row)
			
	numberOfNodes = int(data[0][0])
	radius = float(data[1][0])
	nodesFromFile = data[2:(2+numberOfNodes)]
	edgesFromFile = data[(2+numberOfNodes):]
	print(edgesFromFile)
	
	def createNode(nodeFromFile):
		node = nodeFromFile.split(' ')
		return Node(float(node[1]), float(node[2]), int(node[0]))
	
	def createEdge(edgeFromFile, nodes):
		edge = edgeFromFile.split(' ')
		node1Id = int(edge[0])
		node2Id = int(edge[1])
		node1 = list(filter(lambda x: x.id == node1Id, nodes))[0]
		node2 = list(filter(lambda x: x.id == node2Id, nodes))[0]
		return Edge(node1, node2)
	
	nodes = list(map(lambda x: createNode(x[0]), nodesFromFile))
	edges = list(map(lambda x: createEdge(x[0], nodes), edgesFromFile))
	
	for edge in edges:
		edge.node1.addNeighbour(edge.node2)
		edge.node2.addNeighbour(edge.node1)
	
	return Graph(nodes, edges, radius)
	