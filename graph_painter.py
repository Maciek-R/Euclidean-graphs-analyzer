import networkx as nx
import matplotlib.pyplot as plt

def preparePainterGraph(graph):
	g = nx.Graph()
	g.add_nodes_from(list(map(lambda x: str(x.id), graph.nodes)))
	g.add_edges_from(list(map(lambda x: (str(x.node1.id), str(x.node2.id)), graph.edges)))
	return g
	
def drawPainterGraph(g):
	nx.draw(g, with_labels = True)
	plt.savefig("tmp.png")
	plt.show()