from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
from graph_painter import *

import graph_file_manager as gfm
	
if __name__ == "__main__":
	
	graph = generateGraph(10, 0.45)
	print(graph)
	for node in graph.nodes:
		print(list(map(lambda x: x.id, node.neighbours)))
	
	g = preparePainterGraph(graph)
	drawPainterGraph(g)
	
	print(graph.isConsistent())
	print(graph.getMaxSizeOfConnectedComponent())
	#gfm.writeGraphToFile(graph)
	
	#graphReaded = gfm.readGraphFromFile(10, 0.5)
	#for node in graphReaded.nodes:
	#	print(list(map(lambda x: x.id, node.neighbours)))
	
	#g = preparePainterGraph(graphReaded)
	#drawPainterGraph(g)
		
	#print(graphReaded)