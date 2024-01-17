import numpy as np
import os

"""
Data format: {theta_0:r_0, theta_1:r_1, .... theta_359: r_359}
"""

class Map:
    def __init__(self, location):
        self.location = location
        self.binary_map = []
        self.grayscale_map = []
    
    def load(self):
        self.binary_map = np.loadtxt(self.location, delimiter=",")
        if np.all(np.isin(self.binary_map, [0, 1])):
            self.grayscale_map = np.copy(self.binary_map)
            self.grayscale_map[self.grayscale_map == 1] = 254
        return self.binary_map

