import networkx as nx
import numpy as np
import query as qr
import cluster as cl
import headSTwig as hst
import load_set as ls

#-------Test part-----------
# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/query2.net")
q = nx.Graph()
q = nx.read_pajek("./Net/query2.net")

# Structure of the data graph
A = ["a1","a2","a3"]
B = ["b1","b2","b3","b4"]
C = ["c1","c2","c3","c4"]
D = ["d1","d2","d3"]
E = ["e1","e2","e3"]
F = ["f1","f2","f3","f4"]

# Division of nodes into different machines
n1 = ["a1","a2","b1","c1","d1","e1","f1"]
n2 = ["a3","b2","b3","c2","d2","e2","f2"]
n3 = ["d3","c4","e3","f3"]
n4 = ["b4","c3","e4","f4"]

# List of the machines
n_i = [n1,n2,n3,n4]

# Creation of dictionary node-label
Clusters = [A,B,C,D,E,F]
clu_name = ["a","b","c","d","e","f"]

j=0
nodes = []
labels = []
for c in Clusters:
    for n in c:
        nodes.append(n)
        labels.append(clu_name[j])
    j += 1
# Dictionary nodes-labels
nodes_labels = dict(zip(nodes,labels))

# Read initial graph
H = nx.Graph()
H = nx.read_pajek("./Net/graph_adj2.net")


#-----------End Test Part------------

K = len(n_i)
cluster_test = cl.create_cluster(H,K)
c_graph = cl.create_cluster_graph(cluster_test,query_test)

# Inizialization bi at first step
H_bi = dict()

T = qr.STwig_composition(q)

roots = []

for t in range(0,len(T)):
    roots.append(T[t].root)

print roots

head_root = hst.headSTwig_selection(query_test,roots)

print head_root

R = []
# Exploration
for m in range(0,K):

    R_i = []
    H_bi = dict()

    print m+1
    graph_i = H.subgraph(nbunch=n_i[m])

    # List of explored labels (it contains multiple occurences for the same label -> it' not a problem"
    Exploration = []

    # Exploration
    for t in T:
        #print "root:", t.root, "    label: ", t.label
        R_qt =  qr.MatchSTwig(graph_i,t.root,t.label,H_bi)
        #print "results:", len(R) , "-->", R
        H_bi = qr.update_H_bi(R_qt, H_bi)

        R_i.append(R_qt)
        #print "bi: ", H_bi
        Exploration.append(t.root)

        for e in t.label:
            Exploration.append(e)

    R.append(R_i)

for m in range(0,K):
    for t in range(0,len(roots)):
        F_kt = ls.load_set(m,roots[t],head_root,query_test,c_graph,n_i)
        print F_kt





