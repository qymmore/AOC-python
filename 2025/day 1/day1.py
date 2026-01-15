import re

def count_zeros(puzzle_input, start = 50, mod = 100):
    """
    the goal is to count how many times the dial points at 0 after applying each rotation in the puzzle input.
    
    * puzzle_input: multiline string containing rotation direction and distance
    * start: starting dial position (default 50 as stated in problem)
    * mod: dial size (default 100 for 0..99 range)
    """
    
    # edge case if start position is not within 0..mod-1
    if not (0 <= start < mod):
        raise ValueError("start position must be within the range of the dial size")
    
    pos = start
    count = 0
    
    # use regex to capture direction and integer distance 
    pattern = re.compile(r'^\s*([LR])\s*(-?\d+)\s*$', re.IGNORECASE)
    
    for raw_line in puzzle_input.splitlines():
        line = raw_line.strip()
        if not line:
            continue  # skip empty lines
        
        match = pattern.match(line)
        if not match:
            raise ValueError(f"Invalid input line: {line}")
        
        direction, distance_str = match.group(1).upper(), match.group(2)
        distance = int(distance_str)
        
        # using modulo avoids the need for iterating per click and handles large distances
        # for left rotations subtract and for right rotations add
        
        if direction == 'L':
            pos = (pos - distance) % mod
        else:
            pos = (pos + distance) % mod
        
        if pos == 0:
            count += 1
            
    return count

with open('input.txt', 'r') as f:
    puzzle_input = f.read()
print(count_zeros(puzzle_input))


def count_all_zeros(rotations, start = 50, mod = 100):
    
    # edge case if start position is not within 0..mod-1
    if not (0 <= start < mod):
        raise ValueError("start position must be within the range of the dial size")
    
    pos = start
    total = 0
    
    dir_map = {'L': -1, 'R': 1}
    
    for token in rotations:
        token = token.strip()
        if not token:
            continue  # skip empty tokens   
        
        # parse direction
        dchar = token[0].upper()
        if dchar not in dir_map:
            raise ValueError(f"Invalid direction in token: {token}")
        direction = dir_map[dchar]
        
        # parse steps
        
        try:
            steps = int(token[1:])
        except Exception as e:
            raise ValueError(f"Invalid steps in token: {token}") from e
        
        if steps < 0:
            raise ValueError(f"Steps must be non-negative in token: {token}")
        
        # if there are 0 steps, no intermediate clicks are occuring so we can skip
        if steps == 0:
            continue
        
        # solve for t in 1..steps such that (pos + direction * t) % mod == 0
        
        t0_mod = (-direction * pos) % mod
        
        t0 = t0_mod if t0_mod != 0 else mod
        
        # if first occurrence is within steps, count it and any subsequent occurrences every modulus steps
        if 1 <= t0 <= steps:
            occurrences = 1 + (steps - t0) // mod
            total += occurrences
        
        # update position after full rotation
        pos = (pos + direction * steps) % mod
        
    return total

with open('input.txt', 'r') as f:
    rotations = f.read().splitlines()
print(count_all_zeros(rotations))