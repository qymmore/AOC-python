'''
Count how many of the available IDs fall in any of the given ranges for fresh produce

1. Read all lines from input and split into 2 parts 
2. Parse the first section into list of (start, end) range tuples
3. Parse the second section into list of available IDs
4. For each available ID, check if it falls within any of the ranges
5. Count and return the total number of available IDs that fall within any range (considered fresh)

'''

def count_fresh_produce(lines):
    # split input at the blank line
    sections = "\n".join(lines).strip().split('\n\n')
    range_lines = sections[0].strip().splitlines()
    id_lines = sections[1].strip().splitlines()
    
    # parse ranges
    
    ranges = []
    for r in range_lines:
        start, end = map(int, r.strip().split('-'))
        ranges.append((start, end))
        
    
    # parse ingredient IDs
    ids = [int(x.strip()) for x in id_lines]
    
    fresh = 0
    for id_ in ids:
        for start, end in ranges:
            if start <= id_ <= end:
                fresh += 1
                break  # no need to check other ranges once found a match
    return fresh

with open('input_day5.txt', 'r') as f:
    file = f.read()
print(count_fresh_produce(file.splitlines()))


# part 2

'''
Count how many unique ingredient IDs are covered by union of all given ranges (may be overlapping)

1. Parse all ranges into list of (start, end) tuples again
2. Sort by start value
3. Merge overlapping ranges so there's no double counting
4. Sum the lengths of each merged range

'''

def count_fresh_ids(lines):
    
    sections = "\n".join(lines).strip().split('\n\n')
    range_lines = sections[0].strip().splitlines()
    ranges = [tuple(map(int, r.split('-'))) for r in range_lines]
    
    ranges.sort(key=lambda x: x[0]) # sort by start value
    
    merged = []
    cur_start, cur_end = ranges[0]
    for start, end in ranges[1:]:
        if start <= cur_end + 1:
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end
    merged.append((cur_start, cur_end))
    
    # count total unique IDs covered in merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1
    return total

with open('input_day5.txt', 'r') as f:
    file = f.read()
print(count_fresh_ids(file.splitlines()))