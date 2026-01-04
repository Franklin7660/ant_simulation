import pygame
import numpy as np
import colorsys

class Interface:
    
    gradient = [
        (0, (0, 0, 0)),   
        (0.001, (0, 0, 60)), 
        (0.1, (255, 0, 0)), 
        (0.5, (255, 255, 0)),
        (1.0, (220, 220, 220))   
    ]
    
    def __init__(self):
        self.win = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
        self.pheromones_surf = pygame.Surface((1920,1080))
        self.color = False
        
        self.create_color_lut()
        
    # Create a color lookup table with 256 entries for values from 0 to 255
    def create_color_lut(self, num_entries=256):
        self.gradient_lut = np.zeros((num_entries, 3), dtype=np.uint8)
        indices, colors = zip(*Interface.gradient)
        indices = np.array(indices) * (num_entries - 1)
        
        for i in range(3):  # R, G, B channels
            self.gradient_lut[:, i] = np.interp(range(num_entries), indices, [color[i] for color in colors])
        

    def update(self, simulation):
        matrix = np.clip(simulation.pheromones, 0, simulation.max_pheromone)
        scale = (255 / simulation.max_pheromone)
        color_indices = (matrix * scale).astype(np.uint8)
        
        if self.color:
        # Map each index in the matrix to an RGB color using the LUT
            color_image = self.gradient_lut[color_indices]
        else:
            color_image = np.stack([color_indices]*3, axis = -1)
        
        # Convert to a Pygame surface
        surface = pygame.surfarray.make_surface(color_image)
                       
        self.win.blit(surface, (0,0))
        
        # matrix_scaled = (matrix * scale).astype(np.uint8)
        # color_surface = np.stack([matrix_scaled]*3, axis=-1)
        
        # surface = pygame.surfarray.make_surface(color_surface)
        
        # if self.saturation > 0:
        #     r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, 1)
        #     tint = (int(r * 255), int(g * 255), int(b * 255))
        #     surface.fill(tint, special_flags=pygame.BLEND_MULT)

        
        



