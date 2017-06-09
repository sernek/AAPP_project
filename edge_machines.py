import networkx as nx
import numpy as np
import query as qr
import cluster_mod as cl
import headSTwig as hst
from load_set import create_load_set
import itertools
import node_label_util
import split_machines_util

#-------Test part-----------

# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/query2.net")
q = nx.Graph()
q = nx.read_pajek("./Net/query2.net")

len_query = len(query_test.nodes())

'''
print "Graphs creation"
graphs = split_machines_util.splitMachines("./Net/wordnet3.net",10)
n_i = []
for g in graphs[0:2]:
    n_i.append(g.nodes())
'''

# Division of nodes into different machines
n1 = ["a1","a2","b1","c1","d1","e1","f1"]
n2 = ["a3","b2","b3","c2","d2","e2","f2"]
n3 = ["d3","c4","e3","f3"]
n4 = ["b4","c3","e4","f4"]

# List of the machines
n_i = [n1,n2,n3,n4]
K = len(n_i)

# Read initial graph
H = nx.Graph()
#H = nx.read_pajek("./Wordnet/wordnet3.net")
H = nx.read_pajek("./Net/graph_adj2.net")

#-----------End Test Part------------

# Dictionary node_label for all the graph
nodes_labels = node_label_util.nodeLabelDict("./Net/graph_adj2")


# Graph with only edges between machines
G_clu = nx.Graph(H)
for i in range(K):
    G_i = H.subgraph(nbunch=n_i[i])
    edges_i = G_i.edges()
    G_clu.remove_edges_from(edges_i)
G_clu.remove_nodes_from(nx.isolates(G_clu))

# STwig class: root,children
class STwig:
    def __init__(self, root, label=None):
        self.root = root
        self.label = label if label is not None else label
    def __repr__(self):
        return "<%s,%s>" % (self.root, self.label)

T = qr.STwig_composition(q)

node_test = "a2"

label = "c"
edge = []
for neigh in G_clu.neighbors(node_test):
    if(nodes_labels.get(neigh) == label and neigh in n_i[1]):
        edge = edge + [neigh]
print edge



