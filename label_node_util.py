'''Gets as input the path to a file .net or .clu (without the fle extension)
and returns a dictionary with the label as key and its node as value
'''

def labelNodeDict( path ):
    
    count = 0
    dic = {}

    with open (path + ".net") as net:
        with open (path + "_adj.clu") as clu:
            nodes = net.readlines()
            del nodes[0]
            nodes.reverse()
 
            for line in clu:
                split = line.replace(" ","")
                if "*" in split:
                    count+=1
                    continue
                if count == 2:
                    break
      
                
                nod = nodes.pop().split(' ')
                      
                if(split.strip('"\n\r') in dic):
                    
                    dic[split.strip('"\n\r')].append(nod[1].strip('"\n\r'))
                else:
                     dic.setdefault(split.strip('"\n\r'),[]).append(nod[1].strip('"\n\r'))
                
    return dic

