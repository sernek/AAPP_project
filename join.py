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

# Dictionary node_label for all the graph
nodes_labels = node_label_util.nodeLabelDict("./Net/graph_adj2")

def join_results(R1,R2):

    Results = []
    for i in R1:
        for j in R2:
            #label_join = [nodes_labels.get(n) for n in i]
            #label_j = [nodes_labels.get(m) for m in j]
            not_common = set(i) ^ set(j)
            not_common_label = [nodes_labels.get(nc) for nc in not_common]
            if((set(i) & set(j)) and len(not_common_label) == len(set(not_common_label))):
                join = list ( set(i) | set(j) )
                #print "join",join
            #if(len(join) == len_query):
                Results.append(join)
    #print Results

    return Results


def join_edge(R1, R1_edges, R2):

    Results = []
    Results_edges = []
    iter = 0
    for i in R1:
        #print "i",i
        edges = R1_edges[iter]
        for j in R2:
            edges = R1_edges[iter]
            #print "j",j
            not_common = set(i) ^ set(j)
            not_common_label = [nodes_labels.get(nc) for nc in not_common]
            if((set(i) & set(j)) and len(not_common_label) == len(set(not_common_label))):
                # order of Stwig is modified
                join = list ( set(i) | set(j) )
                #print "join",join
                new_edges = [[nodes_labels.get(j[0]),nodes_labels.get(j[b])] for b in range(1,len(j))]
                edges = edges + new_edges
                #print "edges",edges
                Results.append(join)
                Results_edges.append(edges)
        iter +=1

    return Results,Results_edges
