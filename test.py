import numpy as np

def update_area(grid, cursor_x, cursor_y, area_size, new_value):
    rows, cols = grid.shape
    half_size = area_size // 2
    
    # Calculate boundaries for the area to update
    start_x = max(cursor_x - half_size, 0)
    end_x = min(cursor_x + half_size + 1, cols)
    start_y = max(cursor_y - half_size, 0)
    end_y = min(cursor_y + half_size + 1, rows)
    
    # Update the area
    grid[start_y:end_y, start_x:end_x] = new_value

# Example grid
grid = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
])

# Define cursor position and area size
cursor_x, cursor_y = 3, 3
area_size = 3
new_value = 3

# Update the area around the cursor
update_area(grid, cursor_x, cursor_y, area_size, new_value)

print(grid)
