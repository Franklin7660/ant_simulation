
import random
import numpy as np
from scipy import ndimage

class Simulation:

    def __init__(self, ant_number=1000, grid_width=1080, grid_height=1920, step_size=1.0,
                 sensor_angle=0.5, sensor_length=20, steering_angle=0.2, madness=0, max_pheromone=1, evaporation=0.005):
        
        # Initialize grid and ant parameters as attributes
        self.ant_number = ant_number
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.step_size = step_size
        self.sensor_angle = sensor_angle
        self.sensor_length = sensor_length
        self.steering_angle = steering_angle
        self.madness = madness
        self.max_pheromone = max_pheromone
        self.evaporation = evaporation
        
        self.deposit_batch = 100
        self.deposit_amount = self.ant_number // self.deposit_batch

        # Initialize diffusion kernel as an attribute (with default if none provided)
        self.diffusion_kernel = np.array([
            [0.025, 0.05, 0.025],
            [0.05,  0.7, 0.05 ],
            [0.025, 0.05, 0.025]
        ], dtype=np.float32)
            

        # Initialize pheromone grid and ant positions with lower precision
        self.pheromones = np.zeros((self.grid_height, self.grid_width), dtype=np.float32)
        self.ants = np.zeros((self.ant_number, 3), dtype=np.float32)  # columns: x, y, direction

        # Randomly initialize ant positions and directions
        self.ants[:, 0] = np.random.randint(0, self.grid_width, self.ant_number)  # x positions
        self.ants[:, 1] = np.random.randint(0, self.grid_height, self.ant_number)  # y positions
        self.ants[:, 2] = np.random.uniform(0, 2 * np.pi, self.ant_number)  # directions

    def update_pheromones(self):
        # Apply diffusion and evaporation to pheromones using the diffusion kernel and evaporation attribute
        self.pheromones = ndimage.convolve(self.pheromones, self.diffusion_kernel, mode='wrap', cval=0.0)         
        self.pheromones *= 1 - self.evaporation

    def update_positions(self):
        # Update ant positions based on direction and speed using step_size attribute
        self.ants[:, 0] = (self.ants[:, 0] + self.step_size * np.cos(self.ants[:, 2])) % self.grid_width
        self.ants[:, 1] = (self.ants[:, 1] + self.step_size * np.sin(self.ants[:, 2])) % self.grid_height

    def update_directions(self):
        # Cache trigonometric calculations for each sensor direction to avoid redundant computations
        sensor_directions = np.stack([self.ants[:, 2] + self.sensor_angle, self.ants[:, 2], self.ants[:, 2] - self.sensor_angle], axis=1)
        cos_sensor = np.cos(sensor_directions)
        sin_sensor = np.sin(sensor_directions)

        # Calculate sensor positions for all ants using cached trigonometric values
        sensor_x = (self.ants[:, 0][:, None] + self.sensor_length * cos_sensor) % self.grid_width
        sensor_y = (self.ants[:, 1][:, None] + self.sensor_length * sin_sensor) % self.grid_height
        
        # Convert to integers and ensure indices stay within bounds
        sensor_x = np.clip(sensor_x.astype(int), 0, self.grid_width - 1)
        sensor_y = np.clip(sensor_y.astype(int), 0, self.grid_height - 1)

        # Sample pheromone values at sensor positions
        left_pheromone = self.pheromones[sensor_y[:, 0], sensor_x[:, 0]]
        front_pheromone = self.pheromones[sensor_y[:, 1], sensor_x[:, 1]]
        right_pheromone = self.pheromones[sensor_y[:, 2], sensor_x[:, 2]]

        # Decision-making: rotate randomly if madness is high, otherwise based on pheromone strength
        random_turns = np.random.rand(self.ant_number) < self.madness


        # Adjust directions based on pheromone strengths if not randomly turning
        left_stronger = left_pheromone > right_pheromone
        right_stronger = right_pheromone > left_pheromone
        self.ants[:, 2] += np.where(~random_turns & left_stronger & (front_pheromone < left_pheromone), self.steering_angle, 0)
        self.ants[:, 2] -= np.where(~random_turns & right_stronger & (front_pheromone < right_pheromone), self.steering_angle, 0)

    def deposit_pheromones(self):     
        x_indices = np.clip(self.ants[:, 0].astype(int), 0, self.grid_width - 1)
        y_indices = np.clip(self.ants[:, 1].astype(int), 0, self.grid_height - 1)

        # Deposit pheromones in the buffer grid
        np.add.at(self.pheromones, (y_indices, x_indices), 1)
        self.pheromones = np.clip(self.pheromones, 0, 5)  # Cap pheromone levels

    def update(self):
        # Perform a full update of all ants using class attributes for parameters
        self.update_directions()
        self.update_positions()
        self.deposit_pheromones()
        self.update_pheromones()
        
    def shuffle_params(self):
        self.sensor_angle = random.uniform(0.01,1)
        self.sensor_length = random.randint(5,40)
        self.steering_angle = random.uniform(-0.1,0.5)
        self.madness = random.uniform(0.2, 0.6)
        self.evaporation = random.uniform(0.001,0.01)
        