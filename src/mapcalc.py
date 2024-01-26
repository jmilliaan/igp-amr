import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation

"""
Data format: {theta_0:r_0, theta_1:r_1, .... theta_359: r_359}
"""

class Map:
    def __init__(self, location):
        self.location = location
        self.binary_map = []
        self.grayscale_map = []
        self.walls = []
        self.current_location = None
        self.load()
        self.find_edge()
    
    def load(self):
        self.binary_map = np.loadtxt(self.location, delimiter=",")
        if np.all(np.isin(self.binary_map, [0, 1])):
            self.grayscale_map = np.copy(self.binary_map)
            self.grayscale_map[self.grayscale_map == 1] = 254
        self.binary_map = gaussian_filter(self.binary_map, sigma=1)
        self.binary_map = binary_erosion(self.binary_map, iterations=1)
        
        return self.binary_map
    
    def get_size(self):
        return self.binary_map.shape

    def visualize_matrix(self):
        '''
        TODO this could be cached as plot and refreshed
        matrix: x,y of the map representation
        location: x,y of the location inside the matrix
        '''
        # Create a figure and a set of subplots
        fig, ax = plt.subplots()

        if self.current_location is not None:
            self.add_point(self.current_location[0], self.current_location[1])

        # Display an image on the axes
        cmap = plt.cm.colors.ListedColormap(['white', 'lime', 'yellow','red','green','red','brown','purple','pink','brown','gray','cyan','black'])
        ax.imshow(self.binary_map, cmap=cmap,vmin=0,vmax=13)

        # Hide grid lines
        ax.grid(True)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()

    def find_edge(self):
        # TODO this might not work should the map be more complex
        rows, cols = len(self.binary_map), len(self.binary_map[0])

        #Add the inner walls
        wall_map = {}
        cur_square = 0
        for i in range(0, rows):
            edge_count = 0
            square_count = 0
            for j in range(0, cols):
                if self.binary_map[i][j] == 1:
                    # Check if the neighboring cells form a rectangle
                    if (((i == 0 or i == rows - 1) or (self.binary_map[i-1][j] == 0 or self.binary_map[i+1][j] == 0))
                        and 
                        ((j == 0 or j == cols -1) or (self.binary_map[i][j-1] == 0 or self.binary_map[i][j+1] == 0))):
                        
                        edge_count += 1
                        if (cur_square+square_count not in wall_map):
                            wall_map[cur_square+square_count] = []
                        wall_map[cur_square+square_count].append((i,j))
                        if edge_count == 2:
                            if len(wall_map[cur_square+square_count]) == 4:
                                cur_square += 1
                            else:
                                square_count += 1
                            edge_count = 0
        for index in wall_map:
            rectangle = wall_map[index]
            self.walls.append((rectangle[0][1],rectangle[0][0],rectangle[1][1],rectangle[1][0]))
            self.walls.append((rectangle[0][1],rectangle[0][0],rectangle[2][1],rectangle[2][0]))
            self.walls.append((rectangle[1][1],rectangle[1][0],rectangle[3][1],rectangle[3][0]))
            self.walls.append((rectangle[2][1],rectangle[2][0],rectangle[3][1],rectangle[3][0]))
        
        # Add the outer walls
        self.walls.append((0,0,len(self.binary_map[0])-1,0))
        self.walls.append((0,0,0,len(self.binary_map)-1))
        self.walls.append((0,len(self.binary_map)-1,len(self.binary_map[0])-1,len(self.binary_map)-1))
        self.walls.append((len(self.binary_map[0])-1,len(self.binary_map)-1,len(self.binary_map[0])-1,0))
   
                    

if __name__ == '__main__':
    mapo = Map('map_source.csv')
    print(mapo.walls)
        
        


