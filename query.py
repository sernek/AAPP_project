import networkx as nx
import matplotlib.pyplot as plt

'''
f_a = 10
f_b = 11
f_c = 12
f_d = 13
f_e = 14
f_b = 15
'''

edge_max = []
f = 10
query = nx.Graph()
query = nx.read_pajek("query.net")
q = nx.Graph()
q = nx.read_pajek("query.net")

#nx.draw(query)
#plt.savefig("query.png")


def STwig(q):

    S = []
    T = []
    f_v = 0
    f_u = 0

    for j in range(10):

        print "iteration number", j+1
        f_max = 0
        # If S is empty
        if(not S):
            # Pick an edge (v, u) such that f(u) + f(v) is the largest
            for e in q.edges_iter():
                v = e[0]
                u = e[1]
                f_v = len(q.neighbors(v))
                f_u = len(q.neighbors(u))
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

        print "edge_max = ", edge_max

        #Add T_v to T
        T.append(v)

        # Add neighbors of v in S
        neighbors_v = q.neighbors(v)
        for neigh_v in neighbors_v:
            S.append(neigh_v)

        # Remove edges in T_v from q
        for n in neighbors_v:
            q.remove_edge(v , n)
            q.remove_edge(n , v)


        if(len(q.neighbors(u)) > 0):

            # Add T_u to T
            T.append(u)

            # Remove edges in T_u from q
            neighbors_u = q.neighbors(u)
            for n in neighbors_u:
                q.remove_edge(u , n)
                q.remove_edge(n , u)

            # Add neighbors of u in S
            for neigh_u in neighbors_u:
                S.append(neigh_u)

            # Remove u , v from S
            if( v in S ):  S.remove(v)
            if( u in S ) : S.remove(u)

        for n in q.nodes_iter():
            if(len(q.neighbors(n))==0 and n in S):
                S = [item for item in S if item != n]

        print "T = ", T
        print "S = ", S
        print

        # When the number of edges is zero, the algorithm can finish
        if(q.number_of_edges()==0): break

    # Return the list of the root of the ordered STwig
    return T

def print_STwig(T):
    print "STwig"
    for root in T:
        print root, query.neighbors(root)
        neighbors_r = query.neighbors(root)
        for n in neighbors_r:
            query.remove_edge(root , n)
            query.remove_edge(n , root)

A = ["a1","a2","a3"]
B = ["b1","b2","b3","b4"]
C = ["c1","c2","c3","c4"]
D = ["d1","d2","d3"]
E = ["e1","e2","e3"]
F = ["f1","f2","f3","f4"]

Clusters = [A,B,C,D,E,F]
clu_name = ["a","b","c","d","e","f"]
j=0
nodes = []
labels = []
for c in Clusters:
    for n in c:
        nodes.append(n)
        labels.append(clu_name[j])
    j +=1
# Dictionary node-label
nodes_labels = dict(zip(nodes,labels))

#STwig-test
root = "d"
Label = ["b","c","e","f"]

graph = nx.Graph()
graph = nx.read_pajek("graph_adj.net")
nx.draw(graph)
plt.savefig("graph.png")

#MatchSTwig funtion (to finish is not complete)
def MatchSTwig(r,L):
    S = []
    R = []
    S = D # initial test (root)
    S_l = []
    for n in S:
        print n
        S_l.append(n)
        c = graph.neighbors(n)
        print c
        for child in c:
            child_label = nodes_labels.get(child)
            if(child_label in  L):
                S_l.append(child)
    return S_l

print MatchSTwig(root,Label)


