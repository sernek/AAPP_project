'''
Join all the results
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

#-------Test part-----------

# Dictionary node_label for all the graph
nodes_labels = node_label_util.nodeLabelDict("./Wordnet/wordnet3")


# Join of two lists of partial results
def join_edge(R1, R1_edges, R2):

    Results = []
    Results_edges = []
    iter = 0
    for i in R1:
        edges = R1_edges[iter]
        for j in R2:
            edges = R1_edges[iter]
            not_common = set(i) ^ set(j)
            not_common_label = [nodes_labels.get(nc) for nc in not_common]
            if((set(i) & set(j)) and len(not_common_label) == len(set(not_common_label))):
                join = list ( set(i) | set(j) )
                new_edges = [[nodes_labels.get(j[0]),nodes_labels.get(j[b])] for b in range(1,len(j))]
                edges = edges + new_edges
                Results.append(join)
                Results_edges.append(edges)
        iter +=1

    return Results,Results_edges
