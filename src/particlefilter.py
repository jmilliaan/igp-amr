import array
import numpy as np
from lidarprocessing import LIDAR
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import correlate,medfilt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from mapcalc import Map
import os

class ParticleFilter:
    def __init__(self, map_location, num_particles=4000):
        self.map_location = map_location
        self.map_object = Map(self.map_location)
        self.map = self.map_object.binary_map
        self.map_size = self.map.shape
        self.num_particles = num_particles
        self.current_location = None
        self.particles_mapping = []
        self.angle = None
        self.particles = self.initialize_particles(self.map)
        angles = np.deg2rad(np.linspace(0, 359, 360))
        self.angle_cos = np.cos(angles) * 1950
        self.angle_sin = np.sin(angles) * 1950
        
    def expand_obstacles_np(self, map_data, expansion_amount):
        rows, cols = map_data.shape
        map_expand = np.zeros((rows, cols), dtype=int)

        # Create a kernel of size (2*expansion_amount + 1) filled with 1s
        kernel = np.ones((2*expansion_amount + 1, 2*expansion_amount + 1), dtype=int)

        # Identify the obstacle indices
        obstacle_indices = np.argwhere(map_data == 1)

        # Expand obstacles
        for row, col in obstacle_indices:
            # Define the region to update
            row_start, row_end = max(row - expansion_amount, 0), min(row + expansion_amount + 1, rows)
            col_start, col_end = max(col - expansion_amount, 0), min(col + expansion_amount + 1, cols)
            
            # Define the corresponding kernel region (in case we're at an edge)
            k_row_start, k_row_end = expansion_amount - min(expansion_amount, row), expansion_amount + min(expansion_amount + 1, rows - row)
            k_col_start, k_col_end = expansion_amount - min(expansion_amount, col), expansion_amount + min(expansion_amount + 1, cols - col)
            
            # Update the map_expand with the kernel
            map_expand[row_start:row_end, col_start:col_end] |= kernel[k_row_start:k_row_end, k_col_start:k_col_end]

        # Expand borders
        map_expand[0:expansion_amount, :] = 1
        map_expand[:, 0:expansion_amount] = 1
        map_expand[rows - expansion_amount:rows, :] = 1
        map_expand[:, cols - expansion_amount:cols] = 1
        return map_expand

    def initialize_particles(self, map_data, map_size=(1250, 1500)):
        # Create particle mapping to map form coordinates to particle index
        self.particles_mapping = np.full((1500, 1250), np.nan)
        if (os.path.exists("particles.csv") and os.path.exists("distance_array.csv")):
            # Load particles from text file
            particles = np.loadtxt("particles.csv", delimiter=",")
            self.num_particles = len(particles)
            self.weights = np.ones(self.num_particles) / self.num_particles
            self.distances = np.loadtxt("distance_array.csv", delimiter=",")
            
            for i in range (len(particles)):
                self.particles_mapping[int(particles[i, 0]), int(particles[i, 1])] = i
            
            return particles
        x_positions = np.arange(0, self.map_size[0], 20)
        y_positions = np.arange(0, self.map_size[1], 20)

        # Create a grid of x and y positions
        x_grid,y_grid = np.meshgrid(x_positions, y_positions)   
        
        # Stack the x and y positions into a single 3D array, then reshape into a 2D array of particles
        particles = np.stack((x_grid.ravel(), y_grid.ravel()), axis=1)

        # Remove particles that are inside walls
        for i in range(len(particles) - 1, -1, -1):  # Iterate backwards to avoid issues with deleting elements
            if (map_data[int(particles[i, 0]), int(particles[i, 1])] == 1):
                particles = np.delete(particles, i, axis=0)
        particles = particles[:, ::-1]  # Reverse columns for easier indexing

        # Create particle mapping to map location to particle
        for i in range (len(particles)):
                self.particles_mapping[int(particles[i, 1]), int(particles[i, 0])] = i

        # Update the amount of num particle
        self.num_particles = len(particles)
        self.weights = np.ones(self.num_particles) / self.num_particles
        
        return particles
    
    def generate_precalculate_data(self):
        '''
        Generate precalculate data for the particle filter
        This includes the particles location, distance array, and intersection points array
        '''
        expanded_map = self.expand_obstacles_np(self.map, 40)
        print(expanded_map.shape)
        print(self.map_size)

        # Save particles as text file
        self.particles = self.initialize_particles(expanded_map)
        np.savetxt("particles.csv", self.particles, delimiter=",")
        print("Particles saved")

        # Calculate distance array
        distance_array = []
        intersection_points_array = []
        for particle in self.particles:
            x = np.repeat(particle[0], 360)
            y = np.repeat(particle[1], 360)
            x2 = self.angle_cos + x
            y2 = self.angle_sin + y
            lines = np.column_stack((x,y,x2, y2))

            intersection_points_array_one = []
            # Calculate lines, intersection points, and distances
            for line in lines:
                intersection_points = self.find_intersection(line, self.map_object.walls)
                intersection_points_array_one.append(intersection_points)
                if intersection_points is None:
                    x1, y1, x2, y2 = line
                    plt.imshow(pf.map, cmap="grey")
                    plt.scatter((x1,x2),(y1,y2), s=3, c="r")
                    plt.show()
            distances = []
            for intersect_point in intersection_points_array_one:
                distances.append(calculate_distance(particle, intersect_point))

            intersection_points_array.append(intersection_points_array_one)
            distance_array.append(distances)

        # Save distance array as text file
        np.savetxt("distance_array.csv", distance_array, delimiter=",")
        print("Distance array saved")

        # Save intersection points array as text file
        intersection_points_array = np.array(intersection_points_array)

        # Save the shape of the array to a text file
        with open("intersection_points_array_shape.txt", "w") as f:
            f.write(','.join(map(str, intersection_points_array.shape)))

        intersection_points_array = intersection_points_array.reshape(-1, intersection_points_array.shape[-1])
        np.savetxt("intersection_points_array.csv", intersection_points_array, delimiter=",")
        print("Intersection points array saved")

        

    def load_intersection_points(self):
        # Load the shape from the text file
        with open("intersection_points_array_shape.txt", "r") as f:
            shape = tuple(map(int, f.read().split(',')))

        # Load the data from the text file
        loaded_data = np.loadtxt("intersection_points_array.csv", delimiter=",")

        # Reshape the loaded data back into the original shape
        loaded_data_3d = loaded_data.reshape(shape)

        return loaded_data_3d

    def update_with_lidar(self, lidar_data):
        for i, particle in enumerate(self.particles):
            # Simulate lidar scan for particle and compare with actual lidar data
            # This requires a detailed understanding of how your LIDAR data maps to the environment
            # Assume a function simulate_lidar(particle, self.map) exists
            if self.distances is not None:
                simulated_scan = self.distances[i]
            else:
                simulated_scan = self.simulate_lidar(particle, self.map_object.walls)
            # self.weights[i] *= np.dot(lidar_data, simulated_scan) / (np.linalg.norm(lidar_data) * np.linalg.norm(simulated_scan))
            # Reshape arrays to 2D as cosine_similarity expects 2D arrays
            correlation = correlate(lidar_data, simulated_scan, mode='same')
            max_correlation = np.max(correlation)
            self.weights[i] *= max_correlation
        self.weights += 1.e-300      # Avoid round-off to zero
        self.weights /= sum(self.weights)  # Normalize

        # Resample particles
        indices = np.random.choice(range(len(self.particles)), size=len(self.particles), p=self.weights)
        self.particles = self.particles[indices]

    def get_surrounding_particle(self, current_location, distance=100):
        particle_array = []
        min_x = max(0, int(current_location[0]) - distance)
        max_x = min(self.map_size[1], int(current_location[0]) + distance)
        min_y = max(0, int(current_location[1]) - distance)
        max_y = min(self.map_size[0], int(current_location[1]) + distance)
    
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if self.particles_mapping[x,y] is not None and not math.isnan(self.particles_mapping[x,y]):
                    # print(self.particles_mapping[x,y],self.particles[int(self.particles_mapping[x,y])])
                    particle_array.append(int(self.particles_mapping[x,y]))
        # print(max_x, min_x, max_y, min_y)
        return particle_array
    
    def update_with_lidar_360(self, lidar_data):
        # Apply median filter for noise reduction
        # lidar_data = medfilt(lidar_data, kernel_size=5)
        euclidean_dist_array = []
        if self.current_location is not None:
            temp_particles = self.get_surrounding_particle(self.current_location, 100)
            for particle in temp_particles:
                # Simulate lidar scan for particle and compare with actual lidar data
                # This requires a detailed understanding of how your LIDAR data maps to the environment
                # Assume a function simulate_lidar(particle, self.map) exists
                if self.distances is not None:
                    simulated_scan = self.distances[particle]
                else:
                    simulated_scan = self.simulate_lidar(self.particles[particle], self.map_object.walls)
                # Precompute all rolls
                lidar_data_rolls = np.array([np.roll(lidar_data, i) for i in range(self.angle-90,180)])
                # Compute all distances at once
                distances = np.linalg.norm(lidar_data_rolls - simulated_scan, axis=1)
                # Append to euclidean_dist_array
                euclidean_dist_array.append(distances)
            euclidean_dist_array = np.array(euclidean_dist_array)
            index_flat = np.argmin(euclidean_dist_array)
            index_flat = np.unravel_index(index_flat, euclidean_dist_array.shape)
            self.angle = index_flat[1]
            self.current_location = self.particles[temp_particles[index_flat[0]]]
        else:
            for i, particle in enumerate(self.particles):
                # Simulate lidar scan for particle and compare with actual lidar data
                # This requires a detailed understanding of how your LIDAR data maps to the environment
                # Assume a function simulate_lidar(particle, self.map) exists
                if self.distances is not None:
                    simulated_scan = self.distances[i]
                else:
                    simulated_scan = self.simulate_lidar(particle, self.map_object.walls)
                # Precompute all rolls
                lidar_data_rolls = np.array([np.roll(lidar_data, i) for i in range(360)])
                # Compute all distances at once
                distances = np.linalg.norm(lidar_data_rolls - simulated_scan, axis=1)
                # Append to euclidean_dist_array
                euclidean_dist_array.append(distances)
            euclidean_dist_array = np.array(euclidean_dist_array)
            index_flat = np.argmin(euclidean_dist_array)
            index_flat = np.unravel_index(index_flat, euclidean_dist_array.shape)
            self.angle = index_flat[1]
            self.current_location = self.particles[index_flat[0]]
            
        
        print(self.current_location)
    

    def update_with_imu(self, imu_data, dt):
        # Predict particles' movement based on IMU data
        # IMU data: [linear_acceleration_x, linear_acceleration_y, angular_velocity_z]
        for particle in self.particles:
            # Update orientation
            particle[2] += imu_data[2] * dt

            # Update position
            particle[0] += imu_data[0] * dt
            particle[1] += imu_data[1] * dt

    def resample(self):
        # Find the index of the particle with the maximum weight
        max_weight_index = np.argmax(self.weights)
        # Use this particle as the starting point for resampling
        start_particle = self.particles[max_weight_index]
        # Resample around this particle
        new_particles = start_particle + np.random.normal(0, 1, size=(self.num_particles, 2))
        # Replace the old particles with the new particles
        self.particles = new_particles
        self.weights = np.ones(len(self.particles)) / len(self.particles)

    def estimate_position(self):
        # Estimate robot's position from particles
        self.current_location= np.average(self.particles, weights=self.weights, axis=0)

    def simulate_lidar(self,particle, walls):
        # Simulate a lidar scan for a given particle and map
        # This is a complex function that depends on the specifics of your LIDAR and environment
        x = np.repeat(particle[0], 360)
        y = np.repeat(particle[1], 360)
        x2 = self.angle_cos + x
        y2 = self.angle_sin + y
        lines = np.column_stack((x,y,x2, y2))

        intersection_points_array = []
        # Calculate lines, intersection points, and distances
        for line in lines:
            intersection_points = self.find_intersection(line, walls)
            intersection_points_array.append(intersection_points)
            if intersection_points is None:
                x1, y1, x2, y2 = line
                plt.imshow(pf.map, cmap="grey")
                plt.scatter((x1,x2),(y1,y2), s=3, c="r")
                plt.show()
        distances = []
        for intersect_point in intersection_points_array:
            distances.append(calculate_distance(particle, intersect_point))
        return distances
    
    def find_intersection(self,line, walls):
        x1, y1, x2, y2 = line
        max_t = float('inf')
        x1_x2 = x1 - x2
        y1_y2 = y1 - y2
        for wall in walls:
            x3, y3, x4, y4 = wall
            denominator = (x1_x2) * (y3 - y4) - (y1_y2) * (x3 - x4)
            if denominator == 0:
                continue  # The lines are parallel
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = -((x1_x2) * (y1 - y3) - (y1_y2) * (x1 - x3)) / denominator
            if 0 <= t <= 1 and 0 <= u <= 1:
                if t < max_t:
                    max_t = t
        if max_t == float('inf'):
            return None  # No intersection found
        intersection_x = x1 + max_t * (x2 - x1)
        intersection_y = y1 + max_t * (y2 - y1)
        return (intersection_x, intersection_y)  # Return the closest intersection, or None if no intersection was found

    
    def run_particle_filter(self, lidar_data):
        if self.distances is None:
            self.update_with_lidar(lidar_data)
            self.estimate_position()
            self.resample()
        else:
            self.update_with_lidar_360(lidar_data)
            # self.estimate_position()

    def update(self):
        self.points.set_data(*self.current_location)
        return self.points,
    
    def create_live_plot(self):
        self.fig, self.ax = plt.subplots()

        # Display the static map
        self.ax.imshow(self.map, cmap="gray")

        # Initial plot
        self.plot_curloc = np.array([0, 0])
        self.points, = self.ax.plot(*self.plot_curloc, 'ro')  # 'ro' makes the points red circles

        self.ani = FuncAnimation(self.fig, self.update, frames=range(10), blit=True)

def calculate_line(position, angle, r=1000):
    x, y = position[0], position[1]
    angle_rad = np.deg2rad(angle)  # Convert angle to radians
    x2 = x + r * np.cos(angle_rad)
    y2 = y + r * np.sin(angle_rad)
    return (x, y, x2, y2)

def convert_lidar_data_to_coordinates(lidar_data):
    # Convert to polar coordinates
    # Assume lidar_data is a 2D array where each row is a data point (x, y)
    r = np.sqrt(lidar_data[:, 0]**2 + lidar_data[:, 1]**2)
    theta = np.arctan2(lidar_data[:, 1], lidar_data[:, 0])
    lidar_data = np.column_stack((r, theta))

    return lidar_data

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
def test_pf():
    map_size = (1500, 1250)
    pf = ParticleFilter('map_source.csv')
    # pf.generate_precalculate_data()
    # lidar = LIDAR('COM4')
    lidar_sample = np.loadtxt("map_source/lidar100.csv", delimiter=",")
    intersect_point_data = pf.load_intersection_points()
    
    plt.ion()
    fig, ax = plt.subplots()
    ax.imshow(pf.map, cmap="grey")
    # ax1.scatter(pf.particles[:, 0], pf.particles[:, 1], s=10, c="y")
    location = ax.scatter(0, 0, s=10, c="r")
    # intersections = ax.scatter(intersect_point_data[0,:,0], intersect_point_data[0,:,1], s=10, c="y")
    for scan in lidar_sample:
        pf.run_particle_filter(scan)
        # pf.run_particle_filter(np.array(list(scan.values())))
    #     pf.run_particle_filter(scan)
    #     # np.array(list(scan.values()))
        # ax2.scatter(pf.current_location[0], pf.current_location[1], s=10, c="y")
        location.set_offsets(pf.current_location)
        # intersections.set_offsets(intersect_point_data[scan])
        # ax2.scatter(intersect_point_data[scan][0], intersect_point_data[scan][1].T, s=10, c="r")
        plt.draw()
        plt.pause(0.2)
    plt.ioff()

if __name__ == '__main__':
    map_size = (1500, 1250)
    pf = ParticleFilter('map_source.csv')
    # pf.generate_precalculate_data()
    lidar = LIDAR('COM4')
    lidar_sample = np.loadtxt("map_source/lidar100.csv", delimiter=",")
    intersect_point_data = pf.load_intersection_points()
    
    plt.ion()
    fig, ax = plt.subplots()
    ax.imshow(pf.map, cmap="grey")
    # ax1.scatter(pf.particles[:, 0], pf.particles[:, 1], s=10, c="y")
    location = ax.scatter(0, 0, s=10, c="r")
    # intersections = ax.scatter(intersect_point_data[0,:,0], intersect_point_data[0,:,1], s=10, c="y")
    for scan in lidar.get_lidar_scan():
        pf.run_particle_filter(np.array(list(scan.values())))
    #     pf.run_particle_filter(scan)
    #     # np.array(list(scan.values()))
        # ax2.scatter(pf.current_location[0], pf.current_location[1], s=10, c="y")
        location.set_offsets(pf.current_location)
        # intersections.set_offsets(intersect_point_data[scan])
        # ax2.scatter(intersect_point_data[scan][0], intersect_point_data[scan][1].T, s=10, c="r")
        plt.draw()
        plt.pause(0.01)
    plt.ioff()