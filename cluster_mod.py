import networkx as nx
import node_label_util


# TODO: - put def
# TODO: - insert parameters of the function
# TODO: - K can be removed -> we can use len(n_i)
# G is the Graph , K is the number of machines, n_i is the list of the nodes of the machines
# and nodes_labels is the dictionary nodes-labels
def create_cluster(G,K,n_i,nodes_labels):

    G_clu = nx.Graph(G)

    # Remove edges of G_clu from edges of the different subgraphs
    for i in range(K):
        # TODO: - check if the created graph is undirected or not
        G_i = G.subgraph(nbunch=n_i[i])
        edges_i = G_i.edges()
        G_clu.remove_edges_from(edges_i)

    # Remove edges with no neighbors
    G_clu.remove_nodes_from(nx.isolates(G_clu))

    # List of edges of G_clu
    clu_edge = G_clu.edges()

    # List of couples i,j machines
    m_ij = []

    # List of couple a,b labels
    labels = []

    # Create couple (m_ij,labels) (possible two or more lables for the same couple of machines)
    # There are only two for loops !!!
    for e in clu_edge:
        for i in range(0,K):
            if(e[0] in n_i[i]): m = i
            if(e[1] in n_i[i]): n = i
        # The nodes have to be in two different machines
        if( m != n ):

            # Labels of the nodes of the edge
            a = nodes_labels.get(e[0])
            b = nodes_labels.get(e[1])

            # Useful to keep items in order
            if(m<n):
                m_ij.append((m+1,n+1))
                labels.append([a,b])
            else:
                m_ij.append((n+1,m+1))
                labels.append([b,a])

    # List of list of couple of labels for all the couples of machines
    list_labels = []

    # Create lists for the dictionary machines-labels
    for m in range(0,len(m_ij)):
        # List of couples of labels for each couple of machines
        list_labels_i = []
        list_labels_i.append(labels[m])
        for n in range(0,len(m_ij)):
            if(m_ij[m] == m_ij[n] and m!=n):
                list_labels_i.append(labels[n])
        list_labels.append(list_labels_i)

    # Dictionary machines-list of labels
    machines_labels = dict(zip(m_ij,list_labels))

    return machines_labels


# It takes the dictionary machines_list labels(cluster) and the query graph
# It returns a graph following the rules of the cluster graph
def create_cluster_graph(cluster,query):

    # Inizialization of the cluster graph
    Cluster_graph = nx.Graph()
    # List of edges of the cluster graph
    clu_graph_edges = []

    # TODO: - try to remove some for cycles

    for comb in cluster:
        for e in query.edges():
            for c in cluster.get(comb):
                # TODO: - try to modify the equal for edges
                if ((e[0] == c[0] and e[1] == c[1] or (e[0] == c[1] and e[1] == c[0]))):
                    clu_graph_edges.append(comb)

    clu_graph_edges = list(set(clu_graph_edges))

    # Create cluster graph starting from the useful edges
    Cluster_graph.add_edges_from(clu_graph_edges)

    return Cluster_graph


#-------- Test -----------
'''
cluster_test = create_cluster(H,K)
c_graph = create_cluster_graph(cluster_test,query_test)
'''

