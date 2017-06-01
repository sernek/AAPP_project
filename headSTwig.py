import numpy as np 
import networkx as nx 

query = nx.Graph()
query = nx.read_pajek("./Net/query2.net")

#M = np.matrix

nodes = query.nodes()

for i in range(0, len(nodes)):
    for j in range(0,len(nodes)):
        d = nx.shortest_path_length(query,nodes[i],nodes[j])
        print d