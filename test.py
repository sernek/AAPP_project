import networkx as nx
import matplotlib.pyplot as plt

G = nx.path_graph(20)
G1 = nx.Graph(G)
nx.write_pajek(G1, "wordnettest.net")
G1 = nx.read_pajek("./Wordnet/wordnet3.net")
#G1=nx.read_pajek("testnet.net")
print 'ciao'
nx.draw(G1)
print 'ciao'
plt.savefig("path.png")
#plt.show()




