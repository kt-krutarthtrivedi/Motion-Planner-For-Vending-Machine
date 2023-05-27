import math
import numpy as np
from matplotlib import pyplot as plt

class Can:
    def __init__(self, fig, ax, center=(0, 0, 0), radius=52/2, height=122, roll=0, pitch=0, yaw=0, circle_spacing=8, height_spacing=2):
        self.fig = fig
        self.ax = ax
        self.center = center #in mm
        self.radius = radius #in mm
        self.height = height #in mm
        self.roll = math.radians(roll)
        self.pitch = math.radians(pitch)
        self.yaw = math.radians(yaw)
        self.circle_spacing = circle_spacing
        self.height_spacing = height_spacing
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.visual = 0

    def update_can_points(self):
        cylinder_z = np.linspace(-self.height / 2, self.height / 2, self.height_spacing)
        cylinder_theta = np.linspace(0, 2*math.pi, self.circle_spacing)
        theta, z = np.meshgrid(cylinder_theta, cylinder_z)
        x_temp = self.radius*np.cos(theta)
        y_temp = self.radius*np.sin(theta)
        
        #Rotate wrt Z axis
        x = np.array(x_temp)
        y = np.array(y_temp)
        z_temp = np.array(z)
        for i in range(x_temp.shape[0]):
            for j in range(x_temp.shape[1]):
                x[i][j]= math.cos(self.yaw)*x_temp[i][j]-math.sin(self.yaw)*y_temp[i][j]
                y[i][j]= math.sin(self.yaw)*x_temp[i][j]+math.cos(self.yaw)*y_temp[i][j]

        #Rotate wrt Y axis
        x_temp = np.array(x)
        z_temp = np.array(z)
        for i in range(x_temp.shape[0]):
            for j in range(x_temp.shape[1]):
                x[i][j]= math.cos(self.pitch)*x_temp[i][j]+math.sin(self.pitch)*z_temp[i][j]
                z[i][j]= -math.sin(self.pitch)*x_temp[i][j]+math.cos(self.pitch)*z_temp[i][j]

        #Rotate wrt X axis
        y_temp = np.array(y)
        z_temp = np.array(z)
        for i in range(y_temp.shape[0]):
            for j in range(y_temp.shape[1]):
                y[i][j]= math.cos(self.roll)*y_temp[i][j]-math.sin(self.roll)*z_temp[i][j]
                z[i][j]= math.sin(self.roll)*y_temp[i][j]+math.cos(self.roll)*z_temp[i][j]

        x += self.center[0]
        y += self.center[1]
        z += self.center[2]

        self.X = np.array(x)
        self.Y = np.array(y)
        self.Z = np.array(z)

    def update_pose(self, center=(0, 0, 0), roll=0, pitch=0, yaw=0):
        self.center = center
        self.roll = math.radians(roll)
        self.pitch = math.radians(pitch)
        self.yaw = math.radians(yaw)
        self.update_can_points()

    def spawn_can(self):
        self.visual = self.ax.plot_surface(self.X,self.Y,self.Z,alpha=0.5)

    def clear_can(self):
        self.visual.remove()
    
    def set_flag(self, can_point, plane_equation):
        x = can_point[0]
        y = can_point[1]
        z = can_point[2]

        a = plane_equation[0]
        b = plane_equation[1]
        c = plane_equation[2]
        d = plane_equation[3]

        if ((a*x + b*y + c*z + d) > 0):
            return 2
        elif ((a*x + b*y + c*z + d) < 0):
            return -2
        else:
            return 0

    def check_plane_intersection(self,can_slice, world_equation):
        N = len(can_slice[0])
        flag = 0
        for i in range (N):
            can_point = can_slice[0][i], can_slice[1][i], can_slice[2][i]
            if i == 0:
                flag = self.set_flag(can_point, world_equation)
                if flag == 0:
                    return True
            elif self.set_flag(can_point, world_equation) != flag:
                return True
        return flag
            
    def check_window_pass(self, plane, window_params):
        for window in window_params:
            if plane == window.get_window_equation():
                y_bounds = window.get_y_bounds()
                z_bounds = window.get_z_bounds()
                for i in range(self.height_spacing):
                    for j in range(self.circle_spacing):
                        if self.Y[i][j] <= y_bounds[0] or self.Y[i][j] >= y_bounds[1]:
                            return False
                        if self.Z[i][j] <= z_bounds[0] or self.Z[i][j] >= z_bounds[1]:
                            return False
                return True
            else:
                return False
                                

    # def check_collision(self, world_equations, window_params):
    #     N = self.height_spacing
    #     cylinder_lower_plane = [self.X[0], self.Y[0], self.Z[0]]
    #     cylinder_upper_plane = [self.X[N - 1], self.Y[N - 1], self.Z[N - 1]]
    #     for plane in world_equations:
    #         flag1 = self.check_plane_intersection(cylinder_lower_plane, plane)
    #         if flag1 == True:
    #             if self.check_window_pass(plane, window_params) == False:
    #                 return True
    #         flag2 = self.check_plane_intersection(cylinder_upper_plane, plane)
    #         if flag2 == True:
    #             if self.check_window_pass(plane, window_params) == False:
    #                 return True
    #         if flag1 != flag2:
    #             if self.check_window_pass(plane, window_params) == False:
    #                 return True
    #     return False

    def check_collision(self, window_params):
        padding = math.sqrt((self.height/2)**2 + self.radius ** 2)
        valid_x = [(0 + padding, 750 - padding), (750 + padding, 1000 - padding)]
        valid_y = [(0 + padding, 1000 - padding), (0 + padding, 1000 - padding)]
        valid_z = [(0 + padding, 1000 - padding), (0 + padding, 1000 - padding)]
        window_x = [(750 - padding, 750 + padding), (1000 - padding, 1000 + padding)]
        window_y = [window_params[0].get_y_bounds(), window_params[1].get_y_bounds()]
        window_z = [window_params[0].get_z_bounds(), window_params[1].get_z_bounds()]
        # print(window_y)
        # print(window_z)
        for i in range(2):
            if self.center[0] >= valid_x[i][0] and self.center[0] <= valid_x[i][1]:
                if self.center[1] >= valid_y[i][0] and self.center[1] <= valid_y[i][1]:
                    if self.center[2] >= valid_z[i][0] and self.center[2] <= valid_z[i][1]:
                        pass
                    else:
                        return True
                else:
                    return True
            elif self.center[0] >= window_x[i][0] and self.center[0] <= window_x[i][1]:
                if self.center[1] >= window_y[i][0] and self.center[1] <= window_y[i][1]:
                    if self.center[2] >= window_z[i][0] and self.center[2] <= window_z[i][1]:
                        pass
                    else:
                        return True
                else:
                    return True
        return False