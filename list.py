#!/usr/bin/python

ll = ['a', 'b', 'c', 'b', 'd', 'a']
dd = dict()
for var in ll:
  if var not in dd:
    dd[var] = 1
  else:
    dd[var] = dd[var]+1

for k in dd:
  print "%s --> %d" % (k, dd[k])

for k, v in dd.items():
  print "%s --> %d" % (k, v)

listone = [2, 3, 4]
listtwo = [2*i for i in listone if i > 2]
print listtwo 
