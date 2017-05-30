splitted = open('graph_adj.net', 'w')

with open('graph.net') as fp:
    for line in fp:
        split = line.split(' ')
        for i in range(len(split)-1):
            splitted.write(str(split[0]) + ' ' +  str(split[i+1]))
            if (i < (len(split)-2)):
                splitted.write('\n')

