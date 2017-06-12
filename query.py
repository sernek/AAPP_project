import networkx as nx
from itertools import product
import node_label_util


# Dictionary nodes_labels
# TODO: - modify this
nodes_labels = node_label_util.nodeLabelDict("./Net/graph_adj2")
#nodes_labels = node_label_util.nodeLabelDict("./Wordnet/wordnet3")


# STwig class: root,children
class STwig:
    def __init__(self, root, label=None):
        self.root = root
        self.label = label if label is not None else label
    def __repr__(self):
        return "<%s,%s>" % (self.root, self.label)


# Decompose query into STWig and returns an ordered lists of STwig
def STwig_composition(q):

    # Edge(node1,node2) with max f(v)+f(u) values
    edge_max = []

    S = []
    T = []

    # Set f-value to 1 (initial testing)
    f = 1

    # TODO: - modify exit of the cycle
    # TODO: - reduce lines of code of the two conditions

    for j in range(10):

        f_max = 0
        # If S is empty
        if(not S):
            # Pick an edge (v, u) such that f(u) + f(v) is the largest
            for e in q.edges_iter():
                v = e[0]
                u = e[1]

                # TODO: - add popularity of label to f

                f_v = len(q.neighbors(v))/float(f)
                f_u = len(q.neighbors(u))/float(f)
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
                    f_v = len(q.neighbors(v))
                    f_u = len(q.neighbors(u))
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
        for neigh_v in neighbors_v:
            S.append(neigh_v)

        # Add T_v to T
        T_i = STwig(v,neighbors_v)
        T.append(T_i)

        # Remove edges in T_v from q
        for n in neighbors_v:
            q.remove_edge(v , n)
            #q.remove_edge(n , v)


        # If it already exists a "STwig", I choose it and I stop the selection
        nodes_with_children = [n for n in q.nodes_iter() if len(q.neighbors(n))>0]
        if( len(q.edges()) == 2 and len(nodes_with_children) == 3 ):
            nodes_with_2_children = [n for n in q.nodes_iter() if len(q.neighbors(n))==2]
            children = list(set(nodes_with_children) - set(nodes_with_2_children))
            T_i = STwig(nodes_with_2_children[0],children)
            T.append(T_i)

            break

        else:

            if( len(q.neighbors(u)) > 0 ):

                # Remove edges in T_u from q
                neighbors_u = q.neighbors(u)
                for n in neighbors_u:
                    q.remove_edge(u , n)
                    #q.remove_edge(n , u)

                # Add T_u to T
                T_i = STwig(u,neighbors_u)
                T.append(T_i)

                # Add neighbors of u in S
                for neigh_u in neighbors_u:
                    S.append(neigh_u)

            # Remove u , v from S
            if( v in S ) : S.remove(v)
            if( u in S ) : S.remove(u)

            # TODO: - use nx.isolates() for nodes with no neighbors

            for n in q.nodes_iter():
                if( len(q.neighbors(n)) == 0 and n in S ):
                    # Remove multiple occurences of the same node
                    S = [item for item in S if item != n]

            # When the number of edges is zero, the algorithm can finish
            if(q.number_of_edges()==0): break

    # Return the list of the ordered STwig
    return T


# Inizialization bi at first step
# TODO: - fix global variables, maybe pass at each function Exploration and H_bi
#H_bi = dict()

# List of explored labels (it contains multiple occurences for the same label -> it' not a problem"
Exploration = []


# Check if bi are available for the root
def check_bi_root(r,H_bi):
    bi = H_bi.get(r)
    if( r ):
        return bi


# TODO: Check this function!!!
# Check if bi are available for the children and returns them
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
            # If the label is not yet "explored" ?????????????
            if(l not in Exploration):
                bi_l = [c for c in children if nodes_labels.get(c)==l ]

        # Union of the bi
        if( bi_l):
            bi = bi + bi_l

    bi = list(set(bi))

    return bi


# TODO: - save results as STwig???

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


    #print "Nodes with label: ", r, "->", S


    R_n = []
    for n in S:
        # Children of the root with labels in L
        S_l = []
        # Partial results for each node in S (with root)
        R_n = []

        #Children of a node in S
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
        # TODO: lambda function
        for i in R_i:
            i = [n] + list(i)
            R_n.append(i)

        # Add partial results to final resutls
        R = R + R_n


    # TODO: - in case of child nodes with no root, we search this nodes and we add them to the partial results
    '''
    for l in L:
        child = [key for key in nodes_labels if nodes_labels.get(key) == l and key in graph.nodes()]
        for c in child:
            neigh_label = [nodes_labels.get(c_i) for c_i in graph.neighbors(c)]
            if(r not in neigh_label):
                    R_n.append(child)
    '''



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



