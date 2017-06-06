import networkx as nx

# Import data graph
graph_test = nx.Graph()
graph_test = nx.read_pajek("../Net/wordnet3.net")
#nx.draw(graph)
#plt.savefig("graph2.png")