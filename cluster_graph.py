import networkx as nx


G = nx.Graph()
G = nx.read_pajek("graph_adj_M3.net")
a = nx.nodes(G)
print "55" in G