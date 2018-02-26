import random

a = [2,1,64,12,235,12]
zipped = zip(a, [i for i in range(0,len(a))])
zipped.sort()
unzipped = zip(*zipped)
sortednum = unzipped[0]
correspondindex = unzipped[1]
print(sortednum[len(a)-1])
print(correspondindex[len(a)-1])
