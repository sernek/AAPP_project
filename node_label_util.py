#Gets as input the path to a file .net or .clu (without the fle extension)
#and returns a dictionary with the node as key and its label as value
def nodeLabelDict( path ):
    
    count = 0
    offset = 19
    dic = {}

    with open (path + ".net") as net:
        with open (path + "_adj.clu") as clu:
            for line in net:
                split = line.split(' ')
                if "*" in split[0]:
                    count+=1
                    continue
                if count == 2:
                    break
                if len(split) == 2:
                    clu.seek(offset)
                    offset+=9
                    dic[split[1].strip('"\n\r')] = clu.readline().rstrip('\n\r').replace(" ","")
                    

    return dic


# -------Test----------


#dic = nodeLabelDict("./Wordnet/wordnet3")
#print dic.items()[0:100]

