from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
from graph_painter import *
	
if __name__ == "__main__":
	
	graph = generateGraph(10, 0.5)
	print(graph)
	
	g = preparePainterGraph(graph)
	drawPainterGraph(g)
	
	