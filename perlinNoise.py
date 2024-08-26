import matplotlib.pyplot as plt
import numpy as np
from perlin_numpy import generate_fractal_noise_2d

# Set the seed for reproducibility
np.random.seed(0)

# Generate fractal noise
noise = generate_fractal_noise_2d((256, 256), (8, 8), 5)

# Map noise values to terrain types with 1.00 and 0.75 representing stone
def map_noise_to_terrain(noise):
    terrain = np.zeros_like(noise)
    
    terrain[noise >= 0.75] = 3  # Stone for values 0.75 to 1.00
    terrain[np.logical_and(noise >= 0.5, noise < 0.75)] = 3   # Stone
    terrain[np.logical_and(noise >= 0.25, noise < 0.5)] = 2   # Water
    terrain[noise < 0.25] = 2  # Water (covers 0.0 to 0.25)
    terrain[noise < 0.0] = 1   # Grass for values below 0.0
    
    return terrain

# Apply the mapping
terrain_map = map_noise_to_terrain(noise)

# Define the color map for terrain
cmap = plt.cm.colors.ListedColormap(['green', 'blue', 'gray'])  # Grass -> Green, Water -> Blue, Stone -> Gray
bounds = [0, 1, 2, 3]
norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

# Display the terrain map
plt.imshow(terrain_map, cmap=cmap, norm=norm)
plt.colorbar(ticks=[0.5, 1.5, 2.5], format=plt.FuncFormatter(lambda val, loc: ['Grass', 'Water', 'Stone'][loc]))
plt.title("2D Perlin Noise - Terrain Mapping with Stone at 0.75 and 1.00")
plt.show()
