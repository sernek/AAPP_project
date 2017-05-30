import networkx as nx


G = nx.Graph()
G = nx.read_pajek("graph_adj_M3.net")
H = nx.Graph()
H = nx.read_pajek("graph_adj_M4.net")

a = nx.nodes(G)

def nodeList( machine ):
    count = 0
    nodes = []
    with open ("graph_adj_"+ machine + ".net") as f:
        for line in f:
            split = line.split(' ')
            if "*" in split[0]:
                count+=1
            if count == 2:
                break
            if str(split[0]).isdigit():
                nodes.append(str(split[0]))
    return nodes


def getLabel( nodename, machine ):
    flag = 0
    data = []
    with open("graph_adj_"+ machine + ".net") as f: 
        for line in f:
            if '*' in line:
                flag+= 1
            if flag == 2:
                break
            if flag == 1:
                data.append(line)
    index = [x for x in range(len(data)) if nodename in data[x].lower()]
    
    line_offset = []
    offset = 1
    
    with open("graph_adj_"+ machine + ".clu") as f:
        for line in f:
            line_offset.append(offset)
            offset += len(line)
        f.seek(0)
        f.seek(line_offset[index[0]])
        result = f.readline().replace(" ","")    
    return result





list_node_M4 = nodeList("M4")
list_node_M3 = nodeList("M3")

m3 = nx.nodes(G)
m4 = nx.nodes(H)

mtot = m3 + m4
print mtot
allNodes = [(x, y) for x in list_node_M3 for y in list_node_M4]

