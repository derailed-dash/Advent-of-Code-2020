from collections import defaultdict 
  
  
# Defining a dict 
#d = {}
d = defaultdict(dict) 
   
L = [
    "1:Bob:General",
    "2:Fred:Lieutenant",
    "3:Toby:Captain"
]
   
for row in L:
    row_id, name, rank = row.split(":")
    row_id = int(row_id)
    d[row_id][name] = rank

print(d)
print(d[2])
