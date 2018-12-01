from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
from graph_painter import *

import graph_file_manager as gfm
import graph_test as test
	
if __name__ == "__main__":

	#Testing changing number of nodes. Radius is constant.
	test.testNodes(startFrom = 100, endTo = 201, step = 10, radius = 0.2, numberOfTests = 100)
	
	#Testing changing radius. Number of nodes is constant.
	test.testRadius(startFrom = 1, endTo = 10, step = 1, numberOfNodes = 100, numberOfTests = 100)
	
	
	
	#print(test.test(1, 5000, 0.3))
	
	#graph = generateGraph(10, 0.45)
	#print(graph)
	#for node in graph.nodes:
	#	print(list(map(lambda x: x.id, node.neighbours)))
	
	#g = preparePainterGraph(graph)
	#drawPainterGraph(g)
	
	#print(graph.isConsistent())
	#print(graph.getMaxSizeOfConnectedComponent())
	#gfm.writeGraphToFile(graph)
	
	#graphReaded = gfm.readGraphFromFile(10, 0.5)
	#for node in graphReaded.nodes:
	#	print(list(map(lambda x: x.id, node.neighbours)))
	
	#g = preparePainterGraph(graphReaded)
	#drawPainterGraph(g)
		
	#print(graphReaded)