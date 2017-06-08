import networkx as nx
import numpy as np
import random


# Giving the query graph and the root-nodes,
# it returns the root of the Head STwig
def headSTwig_selection(query,roots):

    # List of nodes of query
    nodes = query.nodes()

    # Number of nodes of the query graph
    n = len(nodes)

    # Index of roots in nodes
    roots_id = []
    for r in roots:
        id = nodes.index(r)
        roots_id.append(id)

    # Distance Matrix
    M = np.zeros(shape=(n,n))

    # Fullfil M: computes all the shortest path
    # for each couple of nodes of the query graph
    # TODO: - try to remove one for cycle
    for i in range(0,n):
        for j in range(0,n):
            # For testing
            if(i<j): # it's a simmetric matrix
                d = nx.shortest_path_length(query,nodes[i],nodes[j])
                M[i][j] = d  # + random.randint(0,5)
                M[j][i] = M[i][j]

    # We are interested only in distance between root-nodes
    M = M[roots_id,:]
    M = M[:, roots_id]

    # List of max M_ri,rj for each root
    max_M = []
    for r in range(0,len(roots)):
        max = np.amax(M[r,:])
        max_M.append(max)


    # Index of the min distance
    head_id = max_M.index(min(max_M))

    # Head STwig selection
    # root of the STwig
    head_root = roots[head_id]

    return head_root

#print "root Head STwig: ",headSTwig_selection(query_test,roots_test)



