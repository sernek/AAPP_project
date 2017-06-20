'''
Contain all the steps of the algorithm and a test part for running the code
'''

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


# Graph with only edges between machines
def overlapGraph(H,n_i):
    G_clu = nx.Graph(H)
    for i in range(K):
        G_i = H.subgraph(nbunch=n_i[i])
        edges_i = G_i.edges()
        G_clu.remove_edges_from(edges_i)
    G_clu.remove_nodes_from(nx.isolates(G_clu))

    return G_clu

# Exploration: for each machines it collects the partial result for each subquery and it saves all the result
# in a list of lists called R (a list for each machine containing the list of the union of all the partial results)
R = []
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

# Load set and Join: each machine collects the result from the correct machine containg in R and then
# join the results
def sub_match(K,roots,head_root,query_test,c_graph,list_machines,G_clu):

    for m in range(0,K):

       # Load set and Join: each machine collects the result from the correct machine containg in R
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

           R_k_qi = R_k_qi + R_qi
           R_m.append(R_k_qi)
       R_m = list(itertools.chain.from_iterable(R_m))


       # Reordering partial results
       R_mf = []
       for root in roots:
           r_root = []
           for r in R_m:
               if(nodes_labels.get(r[0])==root):
                   r_root.append(r)
           R_mf.append(r_root)


       # Join of all the partial results
       Results = []
       Results_edges = []
       for i in range(0,len(R_mf)-1):
           if(i == 0):
               edges_r = []
               for r in R_mf[0]:
                   edges = [[nodes_labels.get(r[0]),nodes_labels.get(r[n])] for n in range(1,len(r))]
                   edges_r.append(edges)
               Results,Results_edges = join.join_edge(R_mf[0],edges_r, R_mf[1])
           else:
               Results,Results_edges = join.join_edge(Results, Results_edges, R_mf[i+1])

       # Check correctness of the obtained results
       Final_results = []
       for r in range(0,len(Results_edges)):
           count = 0
           for e in query_test.edges():
               if([e[0],e[1]] in Results_edges[r] or [e[1],e[0]] in Results_edges[r]):
                   count += 1
           if(count == len(query_test.edges())):
               Final_results.append(Results[r])

    return Final_results


#----------------------------------   Test part  -----------------------------------------#


# Read initial graph
H = nx.Graph()
H = nx.read_pajek("./Net/test.net")
#H = nx.read_pajek("./Net/graph_adj2.net")

# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/querywordnet.net")
q = nx.Graph()
q = nx.read_pajek("./Net/querywordnet.net")
len_query = len(query_test.nodes())


# Slip randomly nodes in K machines
graphs = split_machines_util.splitMachines("./Net/test.net",4)
n_i = []
for g in graphs:
    n_i.append(g.nodes())


# Dictionary node_label for all the graph
nodes_labels = node_label_util.nodeLabelDict("./Wordnet/wordnet3")

# Number of machines
K = len(n_i)

# List with index of machines
list_machines = list(range(1,K+1))

# Cluster graph
cluster_test = cl.create_cluster(H,n_i,nodes_labels)
c_graph = cl.create_cluster_graph(cluster_test,query_test)

# Query decomposition and STWig ordering
T = qr.STwig_composition(q)

# Roots of the STWig
roots = [T[t].root for t in range(0,len(T))]

# Root of the head- STwig
head_root = hst.headSTwig_selection(query_test,roots)

G_clu = overlapGraph(H,n_i)

#Exploration
# Partial result of all the machines
R = []
for m in range(0,K):
    graph_i = H.subgraph(nbunch = n_i[m])
    R_i = exploration(T,graph_i)
    R.append(R_i)

# Returns result of subgraph_matching
sub_match(K,roots,head_root,query_test,c_graph,list_machines,G_clu)




