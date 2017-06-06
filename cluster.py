import networkx as nx

'''
# Query graph
query_test = nx.Graph()
query_test = nx.read_pajek("./Net/query2.net")
'''

# Structure of the data graph
A = ["a1","a2","a3"]
B = ["b1","b2","b3","b4"]
C = ["c1","c2","c3","c4"]
D = ["d1","d2","d3"]
E = ["e1","e2","e3"]
F = ["f1","f2","f3","f4"]

# Division of nodes into different machines
n1 = ["a1","a2","b1","c1","d1","e1","f1"]
n2 = ["a3","b2","b3","c2","d2","e2","f2"]
n3 = ["d3","c4","e3","f3"]
n4 = ["b4","c3","e4","f4"]

# List of the machines
n_i = [n1,n2,n3,n4]

# Creation of dictionary node-label
Clusters = [A,B,C,D,E,F]
clu_name = ["a","b","c","d","e","f"]

j=0
nodes = []
labels = []
for c in Clusters:
    for n in c:
        nodes.append(n)
        labels.append(clu_name[j])
    j += 1
# Dictionary nodes-labels
nodes_labels = dict(zip(nodes,labels))

'''
# Read initial graph
H = nx.Graph()
H = nx.read_pajek("./Net/graph_adj2.net")


# List of edges of graph G
#edges= H.edges()

# Number of machines (for scalability)
K = len(n_i)
'''

# TODO: - put def
# TODO: - insert parameters of the function
# G is the Graph and K is the number of machines

def create_cluster(G,K):

    G_clu = nx.Graph(G)
    
    # Remove edges of G_clu from edges of the different subgraphs
    for i in range(K):
        # TODO: -check if the created graph is undirected or not
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

    # Create couple (m_ij,labels) ( possible two or more lables for the same couple of machines)
    # TODO: - try to remove some for cycles
    for e in clu_edge:
        for i in range(0,K):
            for j in range(0,K):
                if(i !=j and e[0] in n_i[i] and e[1] in n_i[j]):

                    # Labels of the nodes of the edge
                    a = nodes_labels.get(e[0])
                    b = nodes_labels.get(e[1])

                    # Useful to keep items in order
                    if(i<j):
                        m_ij.append((i+1,j+1))
                        labels.append([a,b])
                    else:
                        m_ij.append((j+1,i+1))
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
# For drawing
#labels=nx.draw_networkx_labels(Cluster_graph,pos=nx.spring_layout(Cluster_graph))
#nx.draw(Cluster_graph)
#plt.savefig("./Net/clu_graph.png")







