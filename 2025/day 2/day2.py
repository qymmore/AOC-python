
'''
The problem states to find all "invalid" product IDs that appear in the list and a bunch of rules.
An ID is invalid if it repeats itself (e.g., 55, 6464, 123123 are invalid)
'''

def parse_ranges(s):
    """
    Parse the string of integers in the input file (e.g., 11-22, 95-115) and turn them into a list of (L, M) tuples
    Strip the whitespaces and ignore empty segments
    """
    
    ranges = []
    
    for part in s.split(','):
        part = part.strip()
        if not part:
            continue  # skip empty parts
        
        a_str, b_str = part.split('-', 1)
        a_str = a_str.strip()
        b_str = b_str.strip()
        
        try:
            a = int(a_str)
            b = int(b_str)
        except Exception as e:
            raise ValueError(f"Invalid integers in range segment: {part}") from e
        
        ranges.append((a, b))
    
    return ranges

def merge_ranges(ranges):
    """
    Merge overlapping or adjacent ranges 
    Example: [(1, 5), (4, 10), (15, 20)] -> [(1, 10), (15, 20)]
    """
    
    if not ranges:
        return []
    
    ranges_sorted = sorted(ranges)
    
    merged = []
    cur_l, cur_r = ranges_sorted[0]
    for l, r in ranges_sorted[1:]:
        if l <= cur_r + 1:
            cur_r = max(cur_r, r)
        else:
            merged.append((cur_l, cur_r))
            cur_l, cur_r = l, r
    
    merged.append((cur_l, cur_r))
    
    return merged

def digits(n):
    """
    return number of decimal digits of non-negative integer n
    """
    if n == 0:
        return 1
    d = 0
    while n:
        d += 1
        n //= 10
    return d

def sum_arithmetic(a, b):
    """
    Sum integers from a to b inclusive
    Use (a + b) * count // 2 to avoid any floats
    """
    
    count = b - a + 1
    return (a + b) * count // 2

def sum_invalid_ids(input_str):
    """
    * parse ranges
    * merge ranges to ensure uniqueness and no overlaps
    * for each merged range [L,R], for each half-length k (1..floor(d_max/2)):
        - denom = 10^k + 1
        - s_low = max(ceil(L/denom), 10^(k-1))
        - s_high = min(floor(R/denom), 10^k - 1)
        - if s_low <= s_high:
            - sum contribution = (10^k + 1) * sum_{S=s_low..s_high} S
    * accumulate total 
    """
    
    ranges = parse_ranges(input_str)
    merged_ranges = merge_ranges(ranges)
    
    if not merged_ranges:
        return 0
    
    total_sum = 0
    
    max_R = max(r for (_,r) in merged_ranges)
    max_digits = digits(max_R)
    max_k = max_digits // 2 # only even lengths are possible (2k)
    
    pow10 = [1]  # precompute powers of 10 up to k = max_k to fit Python big int
    for _ in range(1, max_k + 1):
        pow10.append(pow10[-1] * 10)
        
    for (L, R) in merged_ranges:
        # for each possible half length k
        for k in range(1, max_k + 1):
            ten_k = pow10[k]
            denom = ten_k + 1
            
            # s must have k digits and no leading zeros
            s_min_digit = pow10[k - 1]
            s_max_digit = ten_k - 1
            
            s_low = (L + denom - 1) // denom  # ceil(L/denom)
            if s_low < s_min_digit:
                s_low = s_min_digit
                
            s_high = R // denom  # floor(R/denom)
            if s_high > s_max_digit:
                s_high = s_max_digit
            
            if s_low <= s_high:
                sum_S = sum_arithmetic(s_low, s_high)
                contribution = denom * sum_S
                total_sum += contribution
    
    return total_sum

with open('input_day2.txt', 'r') as f:
    file = f.read()
print(sum_invalid_ids(file))

# Part 2

from math import ceil, floor, log10

def sum_repeated_ids(ranges, count_each_once=True):
    """
    Sum all integers in the union of a given inclusive range that are exact repititions of their first half.
    e.g., 95-115 has two invalid IDs: 99 and 111
    """
    
    # normalize ranges (low <= high) and sort/merge ranges for efficiency
    normalized = []
    for lo, hi in ranges:
        if lo > hi:
            lo, hi = hi, lo
        normalized.append((int(lo), int(hi)))
    normalized.sort()
    
    # merge any overlapping or contiguous ranges for simpler checks and avoiding double counting
    merged = []
    
    for lo, hi in normalized:
        if not merged:
            merged.append((lo, hi))
        else:
            last_lo, last_hi = merged[-1]
            if lo <= last_hi + 1:
                # overlap or contiguous
                merged[-1][1] = max(last_hi, hi)
            else:
                merged.append([lo, hi])
    
    # convert to tuple range list
    merged_ranges = [(a,b) for a,b in merged]
    if not merge_ranges:
        return 0
    
    global_min = merged_ranges[0][0]
    global_max = merged_ranges[-1][1]
    
    # helper function to check if a number is in any of the merged ranges
    # since merged_ranges is sorted, conduct binary search or do linear scan if fewer ranges
    def in_ranges(n):
        for lo, hi in merged_ranges:
            if lo <= n <= hi:
                return True
            if n < lo:
                return False
        return False
    
    # determine max digit length to consider
    # if global_max == 0 then handle separately
    
    if global_max <= 0:
        return 0
    
    max_digits = int(floor(log10(global_max))) + 1
    
    # use a set to store distinct invalid IDs found 
    found = set()
    
    # for each block length d (digits of repeating block)
    # and repeat count k >= 2 such that n = d * k <= max_digits
    for d in range(1, max_digits + 1):
        # minimal k is 2 (must repeat at least twice)
        max_k = max_digits // d
        if max_k < 2:
            continue
        
        pow_10_d = 10 ** d
        
        # iterate repeat counts
        for k in range(2, max_k + 1):
            total_digits = d * k
            
            pow_10_dk = 10 ** (d * k)
            R = (pow_10_dk - 1) // (pow_10_d - 1)  # repunit factor
            
            # p must be integer, in range [10^(d-1), 10^d - 1]
            # global_min <= p * R <= global_max
            # so p must be in [ceil(global_min / R), floor(global_max / R)]
            p_low = ceil(global_min / R)
            p_high = floor(global_max / R)
            
            # intersection with digit length constraints
            p_min_allowed = 10 ** (d - 1)
            p_max_allowed = pow_10_d - 1
            
            real_lo = max(p_low, p_min_allowed)
            real_hi = min(p_high, p_max_allowed)
            if real_lo > real_hi:
                continue
            
            # iterate possible p values and build numbers num = p * R
            for p in range(real_lo, real_hi + 1):
                num = p * R
                if num < global_min or num > global_max:
                    continue
                found.add(num)
    
    if count_each_once:
        # sum numbers that lie in any range
        total = 0
        for n in found:
            if in_ranges(n):
                total += n
        return total
    else:
        total = 0
        for lo, hi in merged_ranges:
            for n in found:
                if lo <= n <= hi:
                    total += n
        return total
            
with open('input_day2.txt', 'r') as f:
    file = f.read()
print(sum_repeated_ids(parse_ranges(file)))