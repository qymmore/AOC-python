'''
@ = roll of paper
. = empty space

A roll of paper is accessible if it has fewer than 4 rolls in the 8 surrounding cells (N, S, E, W, NE, NW, SE, SW).
Count the number of accessible rolls of paper in the given grid.

Quick approach:

1. Parse the grid into a 2D list
2. For every cell that is a roll: count the number of rolls in all directions and if < 4 then increment total
3. Make sure to handle edge cases (boundaries of the grid)
'''

def accessible_rolls(grid):
    rows, cols = len(grid), len(grid[0])
    accessible = 0
    
    # directions for all 8 surrounding cells
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        count += 1
                if count < 4:
                    accessible += 1
    return accessible

with open('input_day4.txt', 'r') as f:
    file = f.read()
print(accessible_rolls(file.splitlines()))

# part 2

'''
1. Parse the grid into a 2D list
2. Loop until no more rolls can be removed:
    a. For every roll check if it has < 4 neighbors
    b. Mark all accessible rolls for removal in current iteration
    c. Remove them (set to . or something)
    d. Track running total of removed rolls
3. Stop when iteration removes 0 rolls
'''

def total_removable(grid):
    grid = [list(row) for row in grid]  # Convert to mutable list of lists
    rows, cols = len(grid), len(grid[0])
    total_removed = 0
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    while True:
        to_remove = []
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    count = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            count += 1
                    if count < 4:
                        to_remove.append((r, c))
                        
        # no more rolls can be removed
        if not to_remove:
            break 
        
        # remove all accessible rolls
        for r, c in to_remove:
            grid[r][c] = '.'
        
        total_removed += len(to_remove)
    
    return total_removed

with open('input_day4.txt', 'r') as f:
    file = f.read()
print(total_removable(file.splitlines()))