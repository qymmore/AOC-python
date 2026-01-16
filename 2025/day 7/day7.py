'''
S = start point of the beam
. = empty space
^ = splitter

Beam always moves downward and passes through empty spaces
If beam encounters a splitter (^), it splits into two beams: immediate left and immediate right positions below the splitter

Count the total number of times a beam hits a splitter

1. Find start location S
2. Use a queue to simulate beam paths (each element = (row, col) of a beam)
3. While queue not empty:
    a. Move down until hitting a splitter or going out of bounds
    b. If hitting a splitter, increment count and add two new beams to queue (left and right below)
4. Return total count (until all beams processed)

'''

from collections import deque

def count_beam_splits(grid):
    rows, cols = len(grid), len(grid[0])
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r,c)
                break
    
    split_count = 0
    queue = deque([start])
    visited = set()
    
    while queue:
        r, c = queue.popleft()
        
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        nr = r + 1
        if nr >= rows:
            continue
        
        if grid[nr][c] == '^':
            split_count += 1
            if c - 1 >= 0:
                queue.append((nr, c - 1))
            if c + 1 < cols:
                queue.append((nr, c + 1))
        else:
            queue.append((nr, c))
    return split_count

with open('input_day7.txt', 'r') as f:
    file = f.read()
print(count_beam_splits(file.splitlines()))


'''
Part 2

Now the particle can split multiple times, may merge, and multiple paths can lead to same cell
Count all contributions from all incoming beams at each cell

'''

def count_timelines(grid):
    rows, cols = len(grid), len(grid[0])
    
    dp = [[0] * cols for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_row, start_col = r,c
                break
    
    dp[start_row][start_col] = 1
    
    for r in range(start_row, rows - 1):
        for c in range(cols):
            if dp[r][c] == 0:
                continue
            
            nr = r + 1
            if nr >= rows:
                continue
            
            cell_below = grid[nr][c]
            
            if cell_below == '.':
                dp[nr][c] += dp[r][c]
            elif cell_below == '^':
                if nr + 1 < rows:
                    if c - 1 >= 0:
                        dp[nr + 1][c - 1] += dp[r][c]
                    if c + 1 < cols:
                        dp[nr + 1][c + 1] += dp[r][c]
            else:
                continue
                
    total_timelines = 0
    for r in range(rows):
        for c in range(cols):
            if dp[r][c] == 0:
                continue
         
            if r + 1 >= rows:
                total_timelines += dp[r][c]
            elif grid[r+1][c] not in {'.', '^'}:
                total_timelines += dp[r][c]
            # else: beam would still propagate, so skip

    return total_timelines

with open('input_day7.txt', 'r') as f:
    file = f.read()
print(count_timelines(file.splitlines()))
    