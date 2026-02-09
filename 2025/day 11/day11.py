'''
Find the total number of distinct paths between a source node (you) and sink node (out)
We can use DFS with memoization to solve this DAG problem

'''

import collections

def solve_path(input_text):
    # build the adj list
    graph = {}
    for line in input_text.strip().split('\n'):
        parts = line.split(':')
        node = parts[0].strip()
        # get connections and handle empty strings
        connections = [c.strip() for c in parts[1].split() if c.strip()]
        graph[node] = connections

    memo = {}

    def count_paths(current_node):
        # base case (reactor output reached)
        if current_node == 'out':
            return 1
        
        # alternate base case
        if current_node not in graph:
            return 0
        
        if current_node in memo:
            return memo[current_node]
        
        # recursive step: sum paths from all neighbors
        total_paths = 0
        for neighbor in graph[current_node]:
            total_paths += count_paths(neighbor)
        
        memo[current_node] = total_paths
        return total_paths

    # start the search from 'you'
    return count_paths('you')

def solve_all(data):
    return solve_path(data)

with open('input_day11.txt', 'r') as f:
    data = f.read()
    result = solve_all(data)
    print(f"Total distinct paths: {result}")
    
    
'''
Part 2 

Distinct paths must now also go through 'dac' or 'fft'

'''

def solve_path_constraints(input_text):
    #  adjacency list
    graph = collections.defaultdict(list)
    for line in input_text.strip().split('\n'):
        if ':' not in line: continue
        u, v_list = line.split(':')
        graph[u.strip()] = v_list.split()

    # reusable path counter (memoized)
    def count_paths(start, end):
        memo = {}
        def dfs(curr):
            if curr == end: return 1
            if curr not in graph: return 0
            if curr in memo: return memo[curr]
            
            res = sum(dfs(neighbor) for neighbor in graph[curr])
            memo[curr] = res
            return res
        return dfs(start)

    # sequence A: svr -> fft -> dac -> out
    # math logic is (Paths svr to fft) * (Paths fft to dac) * (Paths dac to out)
    path_a = (count_paths('svr', 'fft') * count_paths('fft', 'dac') * count_paths('dac', 'out'))

    # seq B: svr -> dac -> fft -> out
    # (Paths svr to dac) * (Paths dac to fft) * (Paths fft to out)
    path_b = (count_paths('svr', 'dac') * count_paths('dac', 'fft') * count_paths('fft', 'out'))

    return path_a + path_b

def solve_all(data):
    return solve_path_constraints(data)

with open('input_day11.txt', 'r') as f:
    data = f.read()
    result = solve_all(data)
    print(f"Total distinct paths that go through dac and fft: {result}")