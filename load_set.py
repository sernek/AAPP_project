'''
Starting from the cluster graph, it returns the load set for a certain machine and a particular quey
'''

import networkx as nx

# It returns the load set for a machine k for a query with root q_t_root
# using the head STwig (root) head, the query graph, the cluster graph and the list of machines
def create_load_set(k,q_t_root,head,query,cluster_graph,n_i):

    # Load set
    F_kt = []

    for t in n_i:
        if(k != t):
            # Min Distance head_root and q_t_root in query graph
            d = nx.shortest_path_length(query,head,q_t_root)
            # Min Distance machine k and t in cluter graph
            #D_c = nx.shortest_path_length(cluster_graph,k,t)
            try:
                D_c = nx.shortest_path_length(cluster_graph,k,t)
            except (nx.NetworkXNoPath, nx.NetworkXError):
                D_c = 1000

            #if(D_c <= d):
            if(D_c-1 <= d):
                F_kt.append(t)
    return F_kt




