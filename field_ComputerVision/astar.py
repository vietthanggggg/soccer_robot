"""
A* grid planning
author: Atsushi Sakai(@Atsushi_twi)
        Nikos Kanargias (nkana@tee.gr)
See Wikipedia article (https://en.wikipedia.org/wiki/A*_search_algorithm)
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import json
import os

file = os.path.abspath("data.json")

show_animation = True


class AStarPlanner:

    def __init__(self, ox, oy, resolution, rr):
        """
        Initialize grid map for a star planning
        ox: x position list of Obstacles [m]
        oy: y position list of Obstacles [m]
        resolution: grid resolution [m]
        rr: robot radius[m]
        """

        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy)

    class Node:
        def __init__(self, x, y, cost, parent_index):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

    def planning(self, sx, sy, gx, gy):
        """
        A star path search
        input:
            s_x: start x position [m]
            s_y: start y position [m]
            gx: goal x position [m]
            gy: goal y position [m]
        output:
            rx: x position list of the final path
            ry: y position list of the final path
        """

        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 0.0, -1)
        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                              self.calc_xy_index(gy, self.min_y), 0.0, -1)

        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calc_heuristic(goal_node,
                                                                     open_set[
                                                                         o]))
            current = open_set[c_id]

            # show graph
            if show_animation:  # pragma: no cover
                plt.plot(self.calc_grid_position(current.x, self.min_x),
                         self.calc_grid_position(current.y, self.min_y), "xc")
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                                             lambda event: [exit(
                                                 0) if event.key == 'escape' else None])
                if len(closed_set.keys()) % 10 == 0:
                    plt.pause(0.001)

            if current.x == goal_node.x and current.y == goal_node.y:
                print("Find goal")
                goal_node.parent_index = current.parent_index
                goal_node.cost = current.cost
                break

            # Remove the item from the open set
            del open_set[c_id]

            # Add it to the closed set
            closed_set[c_id] = current

            # expand_grid search grid based on motion model
            for i, _ in enumerate(self.motion):
                node = self.Node(current.x + self.motion[i][0],
                                 current.y + self.motion[i][1],
                                 current.cost + self.motion[i][2], c_id)
                n_id = self.calc_grid_index(node)

                # If the node is not safe, do nothing
                if not self.verify_node(node):
                    continue

                if n_id in closed_set:
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  # discovered a new node
                else:
                    if open_set[n_id].cost > node.cost:
                        # This path is the best until now. record it
                        open_set[n_id] = node

        rx, ry = self.calc_final_path(goal_node, closed_set)

        return rx, ry

    def calc_final_path(self, goal_node, closed_set):
        # generate final course
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    @staticmethod
    def calc_heuristic(n1, n2):
        w = 1.0  # weight of heuristic
        d = w * math.hypot(n1.x - n2.x, n1.y - n2.y)
        return d

    def calc_grid_position(self, index, min_position):
        """
        calc grid position
        :param index:
        :param min_position:
        :return:
        """
        pos = index * self.resolution + min_position
        return pos

    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if px < self.min_x:
            return False
        elif py < self.min_y:
            return False
        elif px >= self.max_x:
            return False
        elif py >= self.max_y:
            return False

        # collision check
        if self.obstacle_map[node.x][node.y]:
            return False

        return True

    def calc_obstacle_map(self, ox, oy):
        self.min_x = round(min(ox))
        self.min_y = round(min(oy))
        self.max_x = round(max(ox))
        self.max_y = round(max(oy))
        #print("min_x:", self.min_x)
        #print("min_y:", self.min_y)
        #print("max_x:", self.max_x)
        #print("max_y:", self.max_y)

        self.x_width = round((self.max_x - self.min_x) / self.resolution)
        self.y_width = round((self.max_y - self.min_y) / self.resolution)
        print("x_width:", self.x_width)
        print("y_width:", self.y_width)

        # obstacle map generation
        self.obstacle_map = [[False for _ in range(self.y_width)]
                             for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    if d <= self.rr:
                        self.obstacle_map[ix][iy] = True
                        break

    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)]]

        return motion
def linear(gx,x,y):
    x_axis = np.linspace(gx,90,10)
    coefficients = np.polyfit(x, y, 1)
    #print ('a =', coefficients[0])
    #print ('b =', coefficients[1])

# Let's compute the values of the line...
    polynomial = np.poly1d(coefficients)    
    y_axis = polynomial(x_axis)
    return y_axis

def main():
    print(__file__ + " start!!")

    # with open("data.json", "r") as openfile:
    #     parameter = json.load(openfile)

    with open(file, "r+") as openfile:
        parameter = json.load(openfile)
    
    # Input point
    ball_coordinate = [parameter['ball_x'],parameter['ball_y']]
    robot_state = [parameter['robot_x'],parameter['robot_y'],parameter['robot_theta']]
    e_robot_state = [parameter['enemy_x'],parameter['enemy_y'],parameter['enemy_theta']]

    middle_goal_x = 90
    middle_goal_y = 0
    
    x_linear = [middle_goal_x, ball_coordinate[0]]
    y_linear = [middle_goal_y, ball_coordinate[1]]
    
    # start and goal position
    sx = robot_state[0]  # [cm]
    sy = robot_state[1]  # [cm]
    gx = ball_coordinate[0] # [cm]
    gy = ball_coordinate[1]  # [cm]
    
    grid_size = 10.0  # [cm]
    robot_radius = 5*math.sqrt(2) # [cm]
    
    #CONFIG DISTANCE OF SHOOTING BALL
    x_axis = np.linspace(gx-7,90,10) # -10 for take a run to kick a ball
    first_g = (x_axis[0],round(linear(gx-7,x_linear,y_linear)[0],1))

    
    # enemy's robot
    e_x = int(e_robot_state[0])
    e_y = int(e_robot_state[1])
    e_theta = e_robot_state[2]

    # set obstacle positions
    ox, oy = [], []
    for i in range(-38, 38):
        ox.append(0)
        oy.append(i)
    for i in range(0, 90):
        ox.append(i)
        oy.append(-38)
    for i in range(0, 90):
        ox.append(i)
        oy.append(38)
    for i in range(20, 38):
        ox.append(90)
        oy.append(i)
    for i in range(-38, -20):
        ox.append(90)
        oy.append(i)
    for i in range(90, 100):
        ox.append(i)
        oy.append(20)
    for i in range(90, 100):
        ox.append(i)
        oy.append(-20)
    for i in range(-20, 20):
        ox.append(100)
        oy.append(i)
    for i in range(e_x-6, e_x+6):
        ox.append(i)
        oy.append(e_y-6)
    for i in range(e_x-6, e_x+6):
        ox.append(i)
        oy.append(e_y+6)
    for i in range(e_y-6, e_y+6):
        ox.append(e_x-6)
        oy.append(i)
    for i in range(e_y-6, e_y+6):
        ox.append(e_x+6)
        oy.append(i)

    if show_animation:  # pragma: no cover
        plt.title('A Star Algorithm')
        plt.plot(sx, sy, "s",label="Messi - Soccer Robot")
        plt.plot(first_g[0], first_g[1], "ob", label="point to shoot")
        plt.plot(ox, oy, ".k",label= "fence")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    # FIRST MOVE
    
    print("take a run to "+str(first_g))
    
    a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
    rx, ry = a_star.planning(sx, sy,first_g[0], first_g[1])
    
    rx.reverse()
    ry.reverse()
    
    rx.remove(rx[len(rx)-1])
    ry.remove(ry[len(ry)-1])

    rx.append(first_g[0])
    ry.append(first_g[1])

    rx.append(ball_coordinate[0])
    ry.append(ball_coordinate[1])

    #rx.append(x_linear[0])#middle of the goal
    #ry.append(y_linear[0])

    #rx.append(gx)
    #ry.append(gy)

    rx.remove(rx[0])
    ry.remove(ry[0])
    
    move_point_list=[]
    
    for i in range(len(rx)):
        point=(rx[i],ry[i])
        move_point_list.append(point)
     
    print("FIRST MOVE POINT LIST: with "+str(len(rx))+" point")
    print(move_point_list)

    # dictionary={
    #     "move_point_list": move_point_list
    # }

    with open(file, 'r+') as openfile:
        j = json.load(openfile)
        j['move_point_list'] = move_point_list
        openfile.seek(0)
        json.dump(j,openfile)
        openfile.truncate()

    # with open("data.json", "w") as outfile:
    #     #json.dump(dictionary, outfile)
    #     outfile.write(json_object)

    rx.reverse()
    ry.reverse()
    rx.append(sx)
    ry.append(sy)
    
    if show_animation:  # pragma: no cover
        
        plt.plot( x_linear[0], y_linear[0], 'yo' )
        plt.plot( x_linear[1], y_linear[1], 'go', label="ball")
        plt.plot(x_axis, linear(gx-7,x_linear,y_linear),"-g", label="path to middle goal")
        plt.plot(rx, ry, "-r", label="path to a ball")
        plt.legend(loc="upper left")
        #plt.legend(["fence", "point_to_take_a_run","robot_coordinate"],loc="upper left")
        plt.pause(0.001)
        
        plt.show()


if __name__ == '__main__':
    main()