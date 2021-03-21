import sys

def total_size_all(no):
  size = 0
  for n in no.explored.values():
    size += total_size_all(n)
  return no.size() + size
  
def total_size_next(no):
  size = 0
  n = no
  while n != None:
    size += n.size()
    n = n.next
    
  return size

def estimate_size(no):
  return no.count * no.size()
