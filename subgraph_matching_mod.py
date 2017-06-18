import networkx as nx
import numpy as np
import query as qr
import cluster_mod as cl
import headSTwig as hst
from load_set import create_load_set
import itertools
import node_label_util
import split_machines_util
import join
from STwig import STwig
from datetime import datetime

#-------Test part-----------


startTime = datetime.now()

# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/querywordnet.net")
q = nx.Graph()
q = nx.read_pajek("./Net/querywordnet.net")

len_query = len(query_test.nodes())


print "Graphs creation"
graphs = split_machines_util.splitMachines("./Net/test.net",2)
n_i = []
for g in graphs:
    n_i.append(g.nodes())

'''
# Division of nodes into different machines
n1 = ["a1","a2","b1","c1","d1","e1","f1"]
n2 = ["a3","b2","b3","c2","d2","e2","f2"]
n3 = ["d3","c4","e3","f3"]
n4 = ["b4","c3","e4","f4"]

# List of the machines
n_i = [n1,n2,n3,n4]
'''

# Read initial graph
H = nx.Graph()
H = nx.read_pajek("./Net/test.net")
#H = nx.read_pajek("./Net/graph_adj2.net")

#-----------End Test Part------------

# Dictionary node_label for all the graph
#nodes_labels = node_label_util.nodeLabelDict("./Net/graph_adj2")
nodes_labels = node_label_util.nodeLabelDict("./Wordnet/wordnet3")


# Number of machines
K = len(n_i)

# List with index of machines
list_machines = list(range(1,K+1))

print "Creation cluster graph"
# Cluster graph creaction c-graph
cluster_test = cl.create_cluster(H,n_i,nodes_labels)
c_graph = cl.create_cluster_graph(cluster_test,query_test)
print c_graph.edges()

print "Query dec and head root"
# Query decomposition and STWig ordering
T = qr.STwig_composition(q)
print T

# Roots of the STWig
roots = []
for t in range(0,len(T)):
    roots.append(T[t].root)

#print roots

# Root of the head- STwig
head_root = hst.headSTwig_selection(query_test,roots)

print "head", head_root

# Graph with only edges between machines
G_clu = nx.Graph(H)
# Remove edges of G_clu from edges of the different subgraphs
for i in range(K):
    G_i = H.subgraph(nbunch=n_i[i])
    edges_i = G_i.edges()
    G_clu.remove_edges_from(edges_i)
# Remove edges with no neighbors
G_clu.remove_nodes_from(nx.isolates(G_clu))


print "Exploration"
# Exploration: for each machines it collects the partial result for each subquery and it saves all the result
# in a list of lists called R (a list for each machine containing the list of the union of all the partial results)
R = []
#for m in range(0,K):

def exploration(T,graph_i):

    R_i = []
    H_bi = dict()
    # List of explored labels
    Exploration = []

    # Exploration
    for t in T:
        R_qt =  qr.MatchSTwig(graph_i,t.root,t.label,H_bi)
        H_bi = qr.update_H_bi(R_qt, H_bi)
        R_i.append(R_qt)
        Exploration.append(t.root)
        for e in t.label:
            Exploration.append(e)

    return R_i


#Exploration
R = []
for m in range(0,K):
    graph_i = H.subgraph(nbunch = n_i[m])
    R_i = exploration(T,graph_i)
    R.append(R_i)


print "Load set and Join"
# Load set and Join: each machine collects the result from the correct machine containg in R and then
# it joins the results
for m in range(0,K):

    print m+1

    # Load set
    R_m = []
    for t in range(0,len(roots)):

        R_k_qi = R[m][t]
        F_kt = create_load_set(m+1,roots[t],head_root,query_test,c_graph,list_machines)
        R_qi = []


        for k in F_kt:
            r = R[k-1][t]
            for r_i in r:
                neigh_clu = [n for n in r_i if n in G_clu.nodes()]
                #near = [G_clu.neighbors(c) for c in neigh_clu]


                for c in neigh_clu:


                    neigh = G_clu.neighbors(c)
                    near = [n for n in neigh if n in n_i[m]]
                    edges = [(c,l) for l in near]
                    R_qi.extend(edges)
                    
                    '''
                    print c
                    for neigh in G_clu.neighbors(c):
                        print neigh
                        if neigh in n_i[m]:
                            edge = [c]
                            #if(nodes_labels.get(neigh) not in R[k-1][t]):
                            edge = [neigh] + edge
                            print "edge",edge
                                #print "edge", edge
                            R_qi.append(edge)
                    '''

        R_k_qi = R_k_qi + R_qi
        R_m.append(R_k_qi)

    R_m = list(itertools.chain.from_iterable(R_m))
   

    R_mf = []
    for root in roots:
        r_root = []
        for r in R_m:
            if(nodes_labels.get(r[0])==root):
                r_root.append(r)
        R_mf.append(r_root)

    Results_edges = []

    #print "R_mf",R_mf
    for i in range(0,len(R_mf)-1):
        if(i == 0):
            edges_r = []
            for r in R_mf[0]:
                edges = [[nodes_labels.get(r[0]),nodes_labels.get(r[n])] for n in range(1,len(r))]
                edges_r.append(edges)
            Results,Results_edges = join.join_edge(R_mf[0],edges_r, R_mf[1])
        else:
            Results,Results_edges = join.join_edge(Results, Results_edges, R_mf[i+1])

    #print "Results", Results
    #print Results_edges

    for r in range(0,len(Results_edges)):
        count = 0
        for e in query_test.edges():
            if([e[0],e[1]] in Results_edges[r] or [e[1],e[0]] in Results_edges[r]):
                count += 1
        if(count == len(query_test.edges())):
            print Results[r]




print datetime.now() - startTime