from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
from graph_painter import *

import graph_file_manager as gfm
import graph_test as test
import graph_diagrams
	
if __name__ == "__main__":

	t1 = test.testNumberOfNodes(50, 501, 10, 0.1, 100)
	graph_diagrams.createPngForTestNumberOfNodes(t1, 50, 501, 0.1)
	
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