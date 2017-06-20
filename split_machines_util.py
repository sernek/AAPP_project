'''Splits in K machines the net given by the attribute path
and returns a list of K machines containing the splitted net
'''

import networkx as nx
import random 




def splitMachines( path, K):
 
    net = [[] for i in range(K)]
    machines = []

    G = nx.read_pajek(path)

    for node in G.nodes_iter():
        i = random.randint(0,K-1)
        net[i].append(node)
    
    for b in range(K):
        machines.append(G.subgraph(net[b]))

    return machines

