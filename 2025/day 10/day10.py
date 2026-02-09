'''
Goal is to convert the indicator lights to a target pattern with minimum button presses 
e.g., [.##.] becomes [0,1,1,0]
'''


import re

def solve_machine(line):
    # parse target lights
    target_str = re.search(r'\[(.*?)\]', line).group(1)
    target = [1 if c == '#' else 0 for c in target_str]
    num_lights = len(target)
    
    # parse the buttons
    button_matches = re.findall(r'\((.*?)\)', line)
    buttons = []
    for b in button_matches:
        vec = [0] * num_lights
        for idx in b.split(','):
            vec[int(idx)] = 1
        buttons.append(vec)
    
    num_buttons = len(buttons)
    min_presses = float('inf')
    
    # use recursion with memoization or bitmasking if buttons < 25 since buttons are limited 
    # and you need the minimum number of presses
    
    for i in range(1 << num_buttons):
        current_state = [0] * num_lights
        press_count = 0
        for b_idx in range(num_buttons):
            if (i >> b_idx) & 1:
                press_count += 1
                for light_idx in range(num_lights):
                    current_state[light_idx] ^= buttons[b_idx][light_idx]
        
        if current_state == target:
            min_presses = min(min_presses, press_count)
            
    return min_presses

def solve_all(data):
    total = 0
    for line in data.strip().split('\n'):
        if line:
            total += solve_machine(line)
    return total

with open('input_day10.txt', 'r') as f:
    data = f.read()
    result = solve_all(data)
    print(f"Total minimum presses needed: {result}")


'''
Part 2

Each button press now increments the counters rather than toggle them
Figure out how many times to press each button so that the sum of increments matches target joltage
Using scipy would be a good option here since we're dealing with linear algebra

'''

import re
import numpy as np
from scipy.optimize import linprog

def solve_machine_scipy(line):
    button_matches = re.findall(r'\((.*?)\)', line)
    joltage_match = re.search(r'\{(.*?)\}', line).group(1)
    targets = [int(x) for x in joltage_match.split(',')]
    
    num_buttons = len(button_matches)
    num_counters = len(targets)
    
    c = np.ones(num_buttons)
    A_eq = np.zeros((num_counters, num_buttons))
    
    for btn_idx, btn_str in enumerate(button_matches):
        if btn_str:
            for counter_idx in btn_str.split(','):
                A_eq[int(counter_idx)][btn_idx] = 1
            
    b_eq = targets

    # integrality=1 forces the solver to find the best WHOLE NUMBER solution
    # 0 = continuous (float), 1 = integer
    integrality = np.ones(num_buttons) 

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), 
                  integrality=integrality, method='highs')
    
    if res.success:
        # if integrality=1, res.fun should be an exact integer
        return int(round(res.fun))
    else:
        # if the solver can't find a solution then it might be impossible
        return 0

def solve_part_two(data):
    total = 0
    lines = data.strip().split('\n')
    for line in lines:
        if line.strip():
            total += solve_machine_scipy(line)
    return total

result = solve_part_two(data)
print(f"Part 2 Total: {result}")