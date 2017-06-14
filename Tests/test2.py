splitted = open('../Wordnet/wordnet3_adj2.net', 'w')

with open('../Wordnet/wordnet3_adj.net') as fp:
    for line in fp:
        split = line.split(' ')
        for i in range(len(split)-1):
            splitted.write(str(split[0]) + ' ' +  str(split[i+1]))
            if (i < (len(split)-2)):
                splitted.write('\n')

