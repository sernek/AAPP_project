import networkx as nx
import numpy as np
import query as qr
import cluster as cl
import headSTwig as hst
from load_set import create_load_set
import itertools
import node_label_util

#-------Test part-----------

# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/query5.net")
q = nx.Graph()
q = nx.read_pajek("./Net/query5.net")

len_query = len(query_test.nodes())


# Division of nodes into different machines
n1 = ["a1","a2","b1","c1","d1","e1","f1"]
n2 = ["a3","b2","b3","c2","d2","e2","f2"]
n3 = ["d3","c4","e3","f3"]
n4 = ["b4","c3","e4","f4"]

# List of the machines
n_i = [n1,n2,n3,n4]


# Read initial graph
H = nx.Graph()
H = nx.read_pajek("./Net/graph_adj2.net")

#-----------End Test Part------------

nodes_labels = node_label_util.nodeLabelDict("./Net/graph_adj2")


# STwig class: root,children
class STwig:
    def __init__(self, root, label=None):
        self.root = root
        self.label = label if label is not None else label
    def __repr__(self):
        return "<%s,%s>" % (self.root, self.label)



def merge_subs(lst_of_lsts):
    res = []
    for row in lst_of_lsts:
        for i, resrow in enumerate(res):
            if row[0]==resrow[0]:
                res[i] += row[1:]
                break
        else:
            res.append(row)
    return res


K = len(n_i)

# List with index of machines
list_machines = list(range(1,K+1))

cluster_test = cl.create_cluster(H,K)
c_graph = cl.create_cluster_graph(cluster_test,query_test)

T = qr.STwig_composition(q)
print T

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

    graph_i = H.subgraph(nbunch = n_i[m])

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

    print m+1

    R_m = []
    for t in range(0,len(roots)):
        R_k_qi = R[m][t]
        F_kt = create_load_set(m+1,roots[t],head_root,query_test,c_graph,list_machines)
        R_qi = []
        for k in F_kt:
            r = R[k-1][t]
            for r_i in r:
                R_qi.append(r_i)
        R_k_qi = R_k_qi + R_qi
        R_m.append(R_k_qi)

    R_m = list(itertools.chain.from_iterable(R_m))

    print R[m]

    print R_m

    print

    print "JOIN"

    Results = []

    for i in R_m:
        join = set(i)
        exp = []
        for j in R_m:
            if( nodes_labels.get(i[0]) != nodes_labels.get(j[0]) and set(i) & set(j) and nodes_labels.get(j[0]) not in exp ):
                exp.append(nodes_labels.get(j[0]))
                join = list ( set(join) | set(j) )
            if(len(join) == len_query  and join not in Results):
                Results.append(join)
    print Results














    '''
    R_stwig = []
    for r in R_m:
        if(len(r)>1):
            stwig = STwig(r[0],r[1:])
        else:
            stwig = STwig(r[0],[])
        R_stwig.append(stwig)

    #print R_stwig


    Join = []
    for i in R_stwig:
        for j in R_stwig:
            join = []
            if(j.root in i.label):
                join = [i.root] + i.label + j.label
                Join.append(list(set(join)))

    #print Join
    '''








