import networkx as nx 
import random

G = nx.Graph()
G = nx.read_pajek("./Wordnet/wordnet3.net")
nodes = []

for node in G.nodes_iter():
    i = random.randint(0,7)
    if i == 1:
        nodes.append(node)

H = G.subgraph(nodes)
nx.write_pajek(H,"./Net/test.net")
