'''
Given (x,y) coordinates of red tiles (#) on a grid, choose any 2 red tiles as opposite corners and calculate the area
The tiles inside the rectangle don't have to include red tiles or be any color
Area will be (x2 - x1) * (y2 - y1)
Goal is to find the largest area possible

'''

def largest_area(coords):

    max_area = 0
    num_points = len(coords)
    
    # 2. Iterate through all pairs
    for i in range(num_points):
        x1, y1 = coords[i]
        for j in range(i + 1, num_points):
            x2, y2 = coords[j]
            
            # 3. Calculate INCLUSIVE area
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

