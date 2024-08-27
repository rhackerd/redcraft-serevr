import numpy as np
from noise import pnoise2

class PerlinNoiseVisualizer:
    def __init__(self, scale=60.0, octaves=6, persistence=0.5, lacunarity=2.0):
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        
        # Define the dimensions of the sections you want to generate
        self.section_size = 16

    def _generate_noise(self, x_offset, y_offset, size):
        """ Generate noise for a specific section of the map """
        noise_map = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                noise_map[i][j] = pnoise2((y_offset + i) / self.scale,
                                          (x_offset + j) / self.scale,
                                          octaves=self.octaves,
                                          persistence=self.persistence,
                                          lacunarity=self.lacunarity,
                                          repeatx=size,
                                          repeaty=size,
                                          base=0)
        return noise_map

    def _normalize_map(self, noise_map):
        """ Normalize the noise map to [0, 1] """
        min_val = np.min(noise_map)
        max_val = np.max(noise_map)
        return (noise_map - min_val) / (max_val - min_val)

    def _apply_terrain_mapping(self, normalized_map):
        """ Map normalized values to terrain types: 1 for grass, 2 for water """
        return np.where(normalized_map < 0.50, 2, 1)

    def get_section(self, x: int, y: int, size: int = 16):
        """ Return a specific section of the terrain map as a list of lists """
        if size != self.section_size:
            raise ValueError("Section size must match the defined section size")

        # Generate the noise map for the specific section
        noise_map = self._generate_noise(x, y, size)
        normalized_map = self._normalize_map(noise_map)
        terrain_map = self._apply_terrain_mapping(normalized_map)
        
        # Convert to list of lists
        return terrain_map.tolist()