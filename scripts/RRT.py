import random
from matplotlib.pyplot import figimage
from numpy.lib.function_base import kaiser
from scipy.spatial import cKDTree
import math
from can import *
import heapq

def calc_dist(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)

class RRT:
    def __init__(self,fig, ax, world_equations, window_params, start, goal, max_tree_size=7000, x_free_space_limit=(0, 1500), yz_free_space_limit=(0, 1000), search_range=50):
        self.start = start
        self.goal = goal
        self.max_tree_size = max_tree_size
        self.vertices = []
        self.orientations = []
        self.edges = []
        self.parent = []
        self.local_paths = {}
        self.connectivity = []
        self.tree_size = 0
        self.x_limits = x_free_space_limit
        self.yz_limits = yz_free_space_limit
        self.search_range = search_range
        self.fig = fig
        self.ax = ax
        self.world_equations = world_equations
        self.window_params = window_params

    def initialize_search_graph(self):
        self.vertices.append(self.start)
        self.orientations.append((0, 0, 0))
        self.edges.append([])
        self.parent.append([])
        self.tree_size += 1
    
    def random_sample(self):
        x = random.randint(self.x_limits[0], self.x_limits[1])
        y = random.randint(self.yz_limits[0], self.yz_limits[1])
        z = random.randint(self.yz_limits[0], self.yz_limits[1])
        return (x, y, z)
    
    def find_inbound_point(self, from_point, to_point):
        modulus = calc_dist(from_point, to_point)
        unit_vector = [(to_point[0] - from_point[0]) / modulus, (to_point[1] - from_point[1]) / modulus, (to_point[2] - from_point[2]) / modulus]
        inbound_free_point = (self.search_range * unit_vector[0], self.search_range * unit_vector[1], self.search_range * unit_vector[2])
        inbound_point = (inbound_free_point[0] + from_point[0], inbound_free_point[1] + from_point[1], inbound_free_point[2] + from_point[2])
        return inbound_point

    def find_nearest(self, sample):
        tree = cKDTree(self.vertices)
        dist, index = tree.query(sample, k=1)
        point=sample
        if dist > self.search_range:
            point = self.find_inbound_point(self.vertices[index], sample)
        nearest = self.vertices[index]
        return index, nearest, point

    # def local_planner(self, nearest, sample, object):
    #     pass

    def update_search_graph(self, index, sample, edge=0):
        self.vertices.append(sample[0])
        self.orientations.append(sample[1])
        # self.local_paths[self.vertices[index], sample[0]] = edge
        self.tree_size += 1
        self.edges[index].append(self.tree_size - 1)
        self.edges.append([])
        self.edges[self.tree_size - 1].append(index)
        self.parent.append([])
        self.parent[self.tree_size - 1] = index

    def local_planner(self, can, end):
        step_size = 25
        positions = [-step_size,step_size]
        # orientations = [-step_size,step_size]
        q =[]
        start = can.center
        # vertices = []
        previous = {}
        distance = {}
        # vertices.append(start)
        previous[start] = 'None'
        distance[can.center] = 0
        position = can.center
        orientation = can.roll, can.pitch, can.yaw
        state = position, orientation
        heapq.heappush(q, (distance[start] + calc_dist(start, end), state))
        count = 0
        while(len(q) !=0):
            # count += 1
            # print(count)
            # print(len(q))
            priority, u = heapq.heappop(q)
            possible_states = []
            for pos_x in positions:
                for pos_y in positions:
                    for pos_z in positions:
                        # for pos_roll in orientations:
                        #     for pos_pitch in orientations:
                        #         for pos_yaw in orientations:
                        pos_roll = random.randint(0, 360)
                        pos_pitch = random.randint(0, 360)
                        pos_yaw = random.randint(0,360)
                        possible_center = (u[0][0] + pos_x, u[0][1] + pos_y, u[0][2] + pos_z)
                        # print(possible_center)
                        possible_orientation = (u[1][0] + pos_roll, u[1][1] + pos_pitch, u[1][2] + pos_yaw)
                        can.update_pose(possible_center, possible_orientation[0], possible_orientation[1], possible_orientation[2])
                        can.update_can_points()
                        if can.check_collision(self.world_equations, self.window_params) == False:
                            # print(False)
                            possible_state = possible_center, possible_orientation
                            possible_states.append(possible_state)
            
            for v in possible_states:
                if (v[0] not in distance.keys() or distance[v[0]] > distance[u[0]] + calc_dist(u[0], v[0])):
                    distance[v[0]] = distance[u[0]] + calc_dist(u[0], v[0])
                    previous[v[0]] = u
                    heapq.heappush(q, (distance[v[0]] + calc_dist(v[0], end), v))
            if calc_dist(u[0], end) <= 15 or count >= 10:
                # print(count)
                end = u
                path = self.trace_local_path(state, end, previous)
                return end, path
            count +=1
        return False

    def trace_local_path(self, start, end, previous):
        local_path = []
        # print(end)
        while (end != start):
            # print(end)
            local_path.append(end)
            end = previous[end[0]]
            # print(start, end)
        local_path.append(start)
        local_path.reverse()
        return local_path

    def build_RRT(self):
        can = Can(self.fig, self.ax)
        self.initialize_search_graph()
        while self.tree_size < self.max_tree_size:
            sample = self.random_sample()
            index, nearest, new_prime = self.find_nearest(sample)
            roll = random.randint(0, 90)
            pitch = random.randint(0, 90)
            yaw = random.randint(0, 90)
            can.center = new_prime
            new = new_prime, (roll, pitch, yaw)
            status=can.check_collision(self.window_params)
            # print(status)
            if status == False:
                self.update_search_graph(index, new)
                self.ax.plot([nearest[0], new[0][0]], [nearest[1], new[0][1]], [nearest[2], new[0][2]], color = "black")
            if calc_dist(new_prime, self.goal) < 100:
                self.update_search_graph(self.tree_size - 1, (self.goal, (0,0,0)))
                return True
        return False


    def trace_path(self, can):
        goal_index = self.tree_size - 1
        previous_index = self.parent[goal_index]
        start_index = 0
        path = []
        path.append((self.vertices[goal_index], self.orientations[goal_index]))
        # print(self.vertices[goal_index])
        path.append((self.vertices[previous_index], self.orientations[previous_index]))
        while previous_index != start_index:
            previous_index = self.parent[previous_index]
            path.append((self.vertices[previous_index], self.orientations[previous_index]))
        path.reverse()
        for i in range(len(path)):
            can.clear_can()
            can.update_pose(path[i][0], path[i][1][0], path[i][1][1], path[i][1][2])
            can.update_can_points()
            can.spawn_can()
            plt.pause(0.1)
        for j in range(len(path) - 1):
            self.ax.plot([path[j][0][0], path[j+1][0][0]], [path[j][0][1], path[j+1][0][1]], [path[j][0][2], path[j+1][0][2]], color = "black")


            
            


    