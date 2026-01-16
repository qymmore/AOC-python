'''
Choose two digits (in order) such that when combined they form the largest possible two-digit number.
e.g. 98765432111111 -> 98
'''

def total_max_joltage(lines):
    total = 0
    for line in lines:
        digits = [int(ch) for ch in line.strip()]
        max_right = -1
        max_joltage = 0
        
        # traverse from right to left
        for i in range(len(digits)-1, -1, -1):
            if max_right != -1:
                # form two-digit number which is current digit followed by largest to its right
                val = digits[i] * 10 + max_right
                if val > max_joltage:
                    max_joltage = val
            # update max_right if current digit is larger
            if digits[i] > max_right:
                max_right = digits[i]
        total += max_joltage
    return total

with open('input_day3.txt', 'r') as f:
    file = f.read()
print(total_max_joltage(file.splitlines()))


# part 2

def max_joltage(digits, k = 12):
    stack = []
    n = len(digits)
    for i, d in enumerate(digits):
        rem = n - i - 1  # remaining digits after current
        while stack and stack[-1] < d and len(stack) - 1 + rem + 1 >= k:
            stack.pop()
        stack.append(d)
    return int(''.join(stack[:k]))

def total_output_voltage(banks, k = 12):
    total = 0
    for bank in banks:
        digits = list(bank.strip())
        total += max_joltage(digits, k)
    return total

with open('input_day3.txt', 'r') as f:
    file = f.read()
print(total_output_voltage(file.splitlines()))