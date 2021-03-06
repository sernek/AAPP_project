'''
Contains all the function necessary to decompose the query and find STwigs in a data grah
'''

from itertools import product
import node_label_util, label_node_util
from STwig import STwig



# Dictionary nodes_labels
nodes_labels = node_label_util.nodeLabelDict("./Wordnet/wordnet3")
labels_nodes = label_node_util.labelNodeDict("./Wordnet/wordnet3")


# Decompose query into STWig and returns an ordered lists of STwig
def STwig_composition(q):

    # Edge(node1,node2) with max f(v)+f(u) values
    edge_max = []
    S = []
    T = []
    while( len(q.edges())!=0 ):

        f_max = 0
        if(not S):
            # Pick an edge (v, u) such that f(u) + f(v) is the largest
            for e in q.edges_iter():
                v = e[0]
                u = e[1]
                f_v = len(q.neighbors(v))/float(len(labels_nodes.get(v)))
                f_u = len(q.neighbors(u))/float(len(labels_nodes.get(u)))
                f_vu = f_v + f_u
                if(f_vu > f_max):
                    f_max = f_vu
                    edge_max = [v , u]
        else:
            # Pick an edge (v, u) such that v belongs to S and f(u) + f(v) is the largest
            for e in q.edges_iter():
                v = e[0]
                u = e[1]
                if(v in S):
                    f_v = len(q.neighbors(v))/float(len(labels_nodes.get(v)))
                    f_u = len(q.neighbors(u))/float(len(labels_nodes.get(u)))
                    f_vu = f_v + f_u
                    if(f_vu > f_max):
                        f_max = f_vu
                        edge_max = [v , u]

        v = edge_max[0]
        u = edge_max[1]

        # I want to choose as first the node with more neighbors
        if(len(q.neighbors(v)) < len(q.neighbors(u))):
             v = edge_max[1]
             u = edge_max[0]

        # Add neighbors of v in S
        neighbors_v = q.neighbors(v)
        S.extend(neighbors_v)
        # Add T_v to T
        T_i = STwig(v,neighbors_v)
        T.append(T_i)
        # Remove edges in T_v from q
        edges_remove = [(v,n) for n in neighbors_v]
        q.remove_edges_from(edges_remove)

        if( len(q.neighbors(u)) > 0 ):

            # Remove edges in T_u from q
            neighbors_u = q.neighbors(u)
            edges_remove = [(u,n) for n in neighbors_u]
            q.remove_edges_from(edges_remove)

            # Add T_u to T
            T_i = STwig(u,neighbors_u)
            T.append(T_i)

            # Add neighbors of u in S
            S.extend(neighbors_u)



        # Remove u , v from S
        if( v in S ) : S.remove(v)
        if( u in S ) : S.remove(u)


        for n in q.nodes_iter():
            if( len(q.neighbors(n)) == 0 and n in S ):
                S = [item for item in S if item != n]

        # When the number of edges is zero, the algorithm can finish
        if(len(q.edges())==0): break

    # Return the list of the ordered STwig
    return T


# Inizialization bi at first step
#H_bi = dict()

# List of explored labels (it contains multiple occurences for the same label -> it' not a problem"
Exploration = []


# Checks if bi are available for the root
def check_bi_root(r,H_bi):
    bi = H_bi.get(r)
    if( r ):
        return bi


# Checks if bi are available for the children and returns them
def check_bi_child(children,L,Exploration,H_bi):

    # Binding informations
    bi = []

    for l in L:

        # bi for the label l
        bi_l = H_bi.get(l)

        # If bi are not empty and the label is already "explored" by a previous query
        if ( bi_l and l in H_bi):
            # Intersection between children of a node and bi
            bi_l = list(set(children) & set(bi_l))
        else:
            # If the label is not yet "explored"
            if(l not in Exploration):
                bi_l = [c for c in children if nodes_labels.get(c)==l ]

        # Union of the bi
        if( bi_l):
            bi = bi + bi_l

    bi = list(set(bi))

    return bi


# MatchSTwig function graph: graph r: root, L: labels H_bi: binding information (add binding information)
def MatchSTwig(graph,r,L,H_bi):

    # Final results
    R = []

    # If there are some bi of the root, S is inizializated using bi,
    # else retrieving all the nodes with the label of the root
    bi = check_bi_root(r,H_bi)
    if( bi ):
        S = bi
    else:
        # All nodes with label equals to label of the root
        S = [key for key in nodes_labels if nodes_labels.get(key)==r and key in graph.nodes()]
        # verify last par and key in graph.nodes()

    R_n = []
    for n in S:
        # Children of the root with labels in L
        S_l = []
        # Partial results for each node in S (with root)
        R_n = []

        # Children of a node in S
        children = graph.neighbors(n)

        # Check bi of the children
        # At first query we don't have bi
        if ( H_bi ):
            children = check_bi_child(children,L,Exploration,H_bi)

        for l in L:
            # Children of n with label l in L
            S_li = [c for c in children if nodes_labels.get(c) == l]
            if( S_li ): # if S_li is not empty
                S_l.append(S_li)

        # Partial result for each node in S without the root
        R_i = [item for item in product(*S_l)]

        # Add root to partial results
        for i in R_i:
            i = [n] + list(i)
            R_n.append(i)

        # Add partial results to final resutls
        R = R + R_n

    return R


# Update bi after the process of a new query
def update_H_bi(R,H_bi):

    # List of new labels in R
    H = list(set().union(*R))

    # Add new labels to previous bi
    H = list(set(H + list(set().union(*H_bi.values()))))

    H_label = list(set([nodes_labels.get(n) for n in H]))
    H_i = []

    for l in H_label:
        i = [h for h in H if (nodes_labels.get(h)==l)]
        H_i.append(i)

    # Dictionary bi with label-nodes
    H_dict = dict(zip(H_label,H_i))

    return H_dict



