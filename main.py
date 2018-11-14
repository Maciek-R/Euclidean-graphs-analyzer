from graph_generator import *
import networkx as nx
import matplotlib.pyplot as plt
	
if __name__ == "__main__":
	
	graph = generateGraph(10, 0.5)
	print(graph)
	
	g = nx.Graph()
	
	g.add_nodes_from(list(map(lambda x: str(x.id), graph.nodes)))
	g.add_edges_from(list(map(lambda x: (str(x.node1.id), str(x.node2.id)), graph.edges)))
	
	nx.draw(g, with_labels = True)
	plt.savefig("tmp.png")
	plt.show()
	
	