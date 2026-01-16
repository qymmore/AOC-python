
'''
The problem states to find all "invalid" product IDs that appear in the list and a bunch of rules.
An ID is invalid if it repeats itself (e.g., 55, 6464, 123123 are invalid)
'''

def is_repeated_twice(num):
    s = str(num)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]

def sum_invalid_ids(ranges_str):
    total = 0
    for part in ranges_str.strip().split(','):
        if not part:
            continue
        start, end = map(int, part.split('-'))
        for num in range(start, end + 1):
            if is_repeated_twice(num):
                total += num
    return total    

with open('input_day2.txt', 'r') as f:
    file = f.read()
print(sum_invalid_ids(file))

# Part 2

def is_repeated_pattern(num):
    s = str(num)
    return s in (s + s)[1:-1]

def sum_repeated_ids(ranges_str):
    total = 0
    for part in ranges_str.strip().split(','):
        if not part:
            continue
        start, end = map(int, part.split('-'))
        for num in range(start, end + 1):
            if is_repeated_pattern(num):
                total += num
    return total
            
with open('input_day2.txt', 'r') as f:
    file = f.read()
print(sum_repeated_ids(file))