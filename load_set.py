import networkx as nx
'''
# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/query2.net")

# Cluster graph
clu_edges = [(1, 2), (1, 4), (2, 3), (3, 4)]
Cluster_graph_test = nx.Graph()
Cluster_graph_test.add_edges_from(clu_edges)

# Roots STwig ordered
roots_test = ["d","c","b"]

# Head Stwig (root)
head_test = "d"

# List of machines
n_i = [1,2,3,4]
'''

# It returns the load set for a machine k for a query with root q_t_root
# using the head STwig (root) head, the query graph, the cluster graph and the list of machines
# TODO: - maybe it's better to remove some parameters
def load_set(k,q_t_root,head,query,cluster_graph,n_i):

    # Load set
    F_kt = []

    for t in n_i:
        if(k != t):
            # Min Distance head_root and q_t_root in query graph
            d = nx.shortest_path_length(query,head,q_t_root)
            # Min Distance machine k and t in cluter graph
            D_c = nx.shortest_path_length(cluster_graph,k,t)
            if(D_c <= d):
                F_kt.append(t)
    return F_kt

#print load_set(1,"b",head_test,query_test,Cluster_graph_test)




