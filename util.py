import random

clu = open ("./wordnet3_adj.clu", "w")
clu.write('*Vertices 82670')
for i in range(0,82670):
    clu.write(str(random.randint(1,10)) + '\n')
clu.close()