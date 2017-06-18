import random

clu = open ("./wordnet3_adj.clu", "w")
clu.write('*Vertices 82670\n')
for i in range(0,82670):
    clu.write("       " + str(random.randint(1,9)) + '\n')
clu.close()