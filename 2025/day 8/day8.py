'''
N junction boxes in 3D space with (x, y, z) coordinates
Need to connect 2 closest junction boxes not already in the same circuit (connecting 2 boxes merges their circuits)
Find sizes of all circuits and multiply 3 largest sizes together after 1000 connections made

1. Generate all pairs of junction boxes and their eucledian distances
2. Sort pairs by distance (ascending)
3. Union find/DSU to track circuits and count sizes of each disjoint set (i.e. circuit)
4. Multiply the sizes of the 3 largest circuits after 1000 connections made

'''

from collections import Counter
from itertools import combinations
import math

class DSU:
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n # number of disjoint sets
        
    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]
        
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True

def multiply_largest(coords, num_connections):
    n = len(coords)
    
    edges = []
    
    for (i, a), (j, b) in combinations(enumerate(coords), 2):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        edges.append((dist, i, j))
    
    edges.sort(key = lambda x: x[0]) # Sort edges by distance
    edges = edges[:num_connections]
    
    # union-find to connect closest pairs
    
    dsu = DSU(n)
    for _, i, j in edges:
        dsu.union(i, j)
        
    counts = Counter()
    for i in range(n):
        counts[dsu.find(i)] += 1

    # now multiply the three largest sizes
    
    largest_sizes = sorted(counts.values(), reverse=True)[:3]
    result = 1
    for size in largest_sizes:
        result *= size
    return result

coords = []
with open('input_day8.txt', 'r') as f:
    file = f.read()
    for line in file.splitlines():
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            coords.append((x, y, z))
print(multiply_largest(coords, 1000))


'''
Part 2

Same as before but now continue until all junction boxes are connected (not just 1000 connections)

'''

def all_connections(coords):
    n = len(coords)
    
    edges = []
    
    for (i, a), (j, b) in combinations(enumerate(coords), 2):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        edges.append((dist, i, j))
    
    edges.sort(key = lambda x: x[0]) # Sort edges by distance
    
    # union-find to connect closest pairs
    
    dsu = DSU(n)
    last_pair = None
    
    for _, i, j in edges:
       if dsu.union(i, j):
           last_pair = (i, j)
           # check if all connected
           if dsu.components == 1:
               break
        
    counts = Counter()
    for i in range(n):
        counts[dsu.find(i)] += 1
    
    x1 = coords[last_pair[0]][0]
    x2 = coords[last_pair[1]][0]
    return x1 * x2

coords = []
with open('input_day8.txt', 'r') as f:
    file = f.read()
    for line in file.splitlines():
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            coords.append((x, y, z))
print(all_connections(coords))