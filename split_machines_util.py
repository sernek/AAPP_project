import networkx as nx 
import random 




#Splits in K machines the net given by the attribute path
#and returns a list of K machines containing the splitted net
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



# -------Test----------
'''
result = splitMachines("./Net/graph_adj2.net",4)

for i in result:
    print nx.nodes(i)

'''