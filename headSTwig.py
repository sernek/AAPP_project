'''
Selection of the head STwig using the query and the roots of the STwigs
'''

import networkx as nx
import numpy as np
import random


# Giving the query graph and the root-nodes,
# it returns the root of the Head STwig
def headSTwig_selection(query,roots):

    # List of nodes of query
    nodes = query.nodes()

    # Number of nodes of the query graph
    #n = len(nodes)

    # Index of roots in nodes
    roots_id = [nodes.index(r) for r in roots]

    # Distance matrix between all pair of nodes in the query
    M = nx.floyd_warshall_numpy(query,nodes)

    # We are interested only in distance between root-nodes
    M = M[roots_id,:]
    M = M[:, roots_id]

    # List of max M_ri,rj for each root
    '''
    max_M = []
    for r in range(0,len(roots)):
        max = np.amax(M[r,:])
        max_M.append(max)
    '''
    max_M = [np.amax(M[r,:]) for r in range(0,len(roots))]

    # Index of the min distance
    head_id = max_M.index(min(max_M))

    # Head STwig selection
    # root of the STwig
    head_root = roots[head_id]

    return head_root




