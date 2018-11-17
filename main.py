from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
from graph_painter import *

import graph_file_manager as gfm
	
if __name__ == "__main__":
	
	graph = generateGraph(10, 0.5)
	print(graph)
	
	#g = preparePainterGraph(graph)
	#drawPainterGraph(g)
	
	gfm.writeGraphToFile(graph)
	graphReaded = gfm.readGraphFromFile(10, 0.5)
		
	print(graphReaded)