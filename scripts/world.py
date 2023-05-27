from matplotlib import pyplot as plt
import numpy as np
from can import *

class Window:
    def __init__(self, window_equation, window_center, window_size):
        self.window_equation = window_equation
        self.window_center = window_center
        self.window_size = window_size
        self.y_bounds = [self.window_center[1] - self.window_size / 2 + 25, self.window_center[1] + self.window_size / 2 - 25]
        self.z_bounds = [self.window_center[2] - self.window_size / 2 + 25, self.window_center[2] + self.window_size / 2 - 25]

    def get_window_equation(self):
        return self.window_equation

    def get_y_bounds(self):
        return self.y_bounds
    
    def get_z_bounds(self):
        return self.z_bounds

class World:
    def __init__(self, fig, ax, cube_side_length=1000, window_side_length=150,window_offset=200, spacing=2):
        self.fig = fig
        self.ax = ax
        self.cube_side = cube_side_length
        self.window_side = window_side_length
        self.window_offset = window_offset
        self.spacing = spacing
        self.x = 0
        self.y = 0
        self.z = 0
        # Stores a, b, c, d for each plane with equation as ax + by + cz + d = 0
        self.world_equations = [[1,0,0,0], [1,0,0,-750], [1,0,0,-1000], [0,0,1,0], [0,0,1,-1000], [0,1,0,0], [0,1,0,-1000]]
        # window parameters
        window1 = Window([1, 0, 0, -750], (750, self.cube_side / 2, self.cube_side - self.window_offset), self.window_side)
        window2 = Window([1, 0, 0, -1000], (1000, self.cube_side / 2, self.window_offset), self.window_side)
        self.window = (window1, window2)
    
    def get_window_params(self):
        return self.window

    def get_world_equations(self):
        return self.world_equations

    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def perform_linspace(self, start, end, axis):
        if axis == 'x':
            self.x = np.linspace(start, end, self.spacing)
        elif axis == 'y':
            self.y = np.linspace(start, end, self.spacing)
        elif axis == 'z':
            self.z = np.linspace(start, end, self.spacing)

    def create_mesh(self, offset_value):
        if str(type(self.x)) != "<class 'numpy.ndarray'>":
            Y, Z = np.meshgrid(self.y, self.z)
            X = np.full_like(Y, offset_value)
        elif str(type(self.y)) != "<class 'numpy.ndarray'>":
            X, Z = np.meshgrid(self.x, self.z)
            Y = np.full_like(X, offset_value)
        elif str(type(self.z)) != "<class 'numpy.ndarray'>":
            X, Y = np.meshgrid(self.x, self.y)       
            Z = np.full_like(X, offset_value)
        return X, Y, Z

    def create_plane(self, start1, end1, axis1, start2, end2, axis2, offset_value):
        self.reset()
        self.perform_linspace(start1, end1, axis1)
        self.perform_linspace(start2, end2, axis2)
        X, Y, Z = self.create_mesh(offset_value)
        self.ax.plot_surface(X,Y,Z,alpha=0.5)

    def create_world(self):
        #Create planes
        self.create_plane(0, self.cube_side, 'x', 0, self.cube_side, 'y', 0)
        self.create_plane(0, self.cube_side, 'x', 0, self.cube_side, 'y', 1000)
        self.create_plane(0, self.cube_side, 'y', 0, self.cube_side, 'z', 0)
        self.create_plane(0, self.cube_side, 'y', 0, self.cube_side, 'z', 750)
        self.create_plane(0, self.cube_side, 'y', 0, self.cube_side, 'z', 1000)
        self.create_plane(0, self.cube_side, 'x', 0, self.cube_side, 'z', 0)
        self.create_plane(0, self.cube_side, 'x', 0, self.cube_side, 'z', 1000)
        #Create window
        start1 = (self.cube_side - self.window_side) /2
        end1 = (self.cube_side + self.window_side) /2
        start2 = self.cube_side - self.window_offset - self.window_side / 2
        end2 = self.cube_side - self.window_offset + self.window_side / 2
        self.create_plane(start1, end1, 'y', start2, end2, 'z', 750)
        start2 = self.window_offset - self.window_side / 2
        end2 = self.window_offset + self.window_side / 2
        self.create_plane(start1, end1, 'y', start2, end2, 'z', 1000)

# General Equation of plane is:
# ax + by + cz + d = 0
# If plane normal is [1, 0, 0], then equation of plane is(meaning, y-z plane):
# x + d1 = 0
# In our case, the three planes are :
# x = 0, x - 750 = 0 and x - 1000 = 0
# If plane normal is [0, 1, 0], then equation of plane is(meaning, x-z plane):
# y + d2 = 0
# In our case, the two planes are :
# y = 0 and y - 1000 = 0
# If plane normal is [0, 0, 1], then equation of plane is(meaning, x-y plane):
# z + d3 = 0
# In our case, the two planes are :
# z = 0 and z - 1000 = 0