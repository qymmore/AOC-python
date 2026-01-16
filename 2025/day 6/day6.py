'''
Numbers for each operation are stacked vertically and separated by 1 or more columns
that are all spaces

The operator can be either + or * and goal is to compute the result for each problem
and sum all the results

1. Read all the rows into a 2D character grid
2. Identify the column boundaries where at least 1 character is not a space
3. Extract the digits in the columns and use bottom row for operation
4. Sum all the results and return

'''

def compute_operations(rows):
    grid = [list(row) for row in rows]
    n_rows = len(grid)
    n_cols = len(grid[0])
    
    # identify all non-empty columns
    is_non_empty = [any(grid[r][c] != ' ' for r in range(n_rows)) for c in range(n_cols)]
    
    # identify all columns with problems
    
    problems = []
    c = 0
    
    while c < n_cols:
        if is_non_empty[c]:
            start_c = c
            while c < n_cols and is_non_empty[c]:
                c += 1
            end_c = c  # exclusive
            problems.append((start_c, end_c))
        else:
            c += 1
            
    total_sum = 0
    for start, end in problems:
        numbers = []
        
        # read all rows except the last one which is the operator
        for r in range(n_rows - 1):
            num_str = ''.join(grid[r][start:end]).strip()
            if num_str:
                numbers.append(int(num_str))
        operator = ''.join(grid[n_rows - 1][start:end]).strip()
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for num in numbers:
                result *= num
        else:
            raise ValueError("Unknown operator: {}".format(operator))
        total_sum += result
    return total_sum

with open('input_day6.txt', 'r') as f:
    file = f.read()
print(compute_operations(file.splitlines()))

'''
Part 2

Now numbers are read right-to-left in columns
Top row is most significant digit and bottom row is least significant digit
So need to read digits in reverse order for each column, apply operation, and sum all results

'''

def compute_operations_reversed(rows):
    grid = [list(row) for row in rows]
    n_rows = len(grid)
    n_cols = len(grid[0])
    
    # identify all non-empty columns
    is_non_empty = [any(grid[r][c] != ' ' for r in range(n_rows)) for c in range(n_cols)]
    
    # identify all columns with problems
    
    problems = []
    c = 0
    
    while c < n_cols:
        if is_non_empty[c]:
            start_c = c
            while c < n_cols and is_non_empty[c]:
                c += 1
            end_c = c  # exclusive
            problems.append((start_c, end_c))
        else:
            c += 1
            
    total_sum = 0
    
    for start, end in problems:
        numbers = []
        
        for col in range(start, end):
            num_str = ''.join(grid[r][col] for r in range(n_rows - 1)).strip()
            if num_str:
                numbers.append(int(num_str))
                
        operator_str = ''.join(grid[n_rows - 1][start:end]).strip()
        if operator_str == '+':
            result = sum(numbers)
        elif operator_str == '*':
            result = 1
            for num in numbers:
                result *= num
        else:
            raise ValueError("Unknown operator: {}".format(operator_str))
        total_sum += result
        
    return total_sum

with open('input_day6.txt', 'r') as f:
    file = f.read()
print(compute_operations_reversed(file.splitlines()))
    