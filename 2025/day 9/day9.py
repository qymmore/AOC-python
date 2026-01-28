'''
Given (x,y) coordinates of red tiles (#) on a grid, choose any 2 red tiles as opposite corners and calculate the area
The tiles inside the rectangle don't have to include red tiles or be any color
Area will be (x2 - x1) * (y2 - y1)
Goal is to find the largest area possible

'''

def largest_area(coords):

    max_area = 0
    num_points = len(coords)
    
    # Iterate through all pairs
    for i in range(num_points):
        x1, y1 = coords[i]
        for j in range(i + 1, num_points):
            x2, y2 = coords[j]
            
            # Calculate INCLUSIVE area
            # If x1=2 and x2=5, the tiles are 2, 3, 4, 5 (4 tiles total)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                
    return max_area

points = []

with open('input_day9.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    x, y = map(int, line.split(','))
                    points.append((x, y))

print(largest_area(points))


'''
Part 2 

Now the tiles must be green AND red
'''

def sol_part_two(points):
    max_area = 0
    num_points = len(points)
    
    # create a set of edges for the polygon (checking for intersections)
    edges = []
    for i in range(num_points):
        p1 = points[i]
        p2 = points[(i + 1) % num_points]
        edges.append((p1, p2))

    def is_rect_valid(x1, y1, x2, y2):
        # normalize the coordinates
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        # check if a rectangle is valid in an orthogonal polygon:
        # midpoint of the rectangle must be inside AND
        # no polygon edge can strictly cross the rectangle
        
        mid_x, mid_y = (min_x + max_x) / 2, (min_y + max_y) / 2
        
        # Ray casting for the midpoint (thanks gemini)
        inside = False
        for (px1, py1), (px2, py2) in edges:
            # Only need to check vertical edges for ray casting
            if px1 == px2: # Vertical edge
                if min(py1, py2) <= mid_y < max(py1, py2):
                    if mid_x < px1:
                        inside = not inside
        
        if not inside:
            return False

        # check if any edges cut through the rectangle
        for (px1, py1), (px2, py2) in edges:
            if px1 == px2: # Vertical edge
                if min_x < px1 < max_x:
                    if not (max(py1, py2) <= min_y or min(py1, py2) >= max_y):
                        return False
            else: # Horizontal edge
                if min_y < py1 < max_y:
                    if not (max(px1, px2) <= min_x or min(px1, px2) >= max_x):
                        return False
        return True

    # iterate through pairs of red tiles
    for i in range(num_points):
        for j in range(i + 1, num_points):
            x1, y1 = points[i]
            x2, y2 = points[j]
                   
            # check validity before calculating area
            if is_rect_valid(x1, y1, x2, y2):
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                max_area = max(max_area, width * height)
                
    return max_area

points = []

with open('input_day9.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    x, y = map(int, line.split(','))
                    points.append((x, y))

print(sol_part_two(points))