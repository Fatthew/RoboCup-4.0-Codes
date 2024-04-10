import numpy as np
import matplotlib.pyplot as plt
from heapq import heappop, heappush
import random

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2) #cost function

def astar(start, goal):
    open_list = []
    closed_set = set()

    heappush(open_list, (0, start))

    while open_list:
        _, current = heappop(open_list)
        
        if current.x == goal.x and current.y == goal.y:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add((current.x, current.y))

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]: #define possible movements
            x, y = current.x + dx, current.y + dy

            if -199 <= x <= 199 and -199 <= y <= 199 and (x, y) not in closed_set:
                neighbor = Node(x, y)
                neighbor.parent = current
                neighbor.g = current.g + 1 #tally cost of path
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                heappush(open_list, (neighbor.f, neighbor))
                closed_set.add((x, y))

    return None

def calculate_rotation(current_heading, desired_heading): #determine rotation required
    current_heading = current_heading % 360 #ensure value is 0 < x <360
    desired_heading = desired_heading % 360 #ensure value is 0 < x <360

    #calculate rotation in both directions and choose best
    counterclockwise_rotation = (desired_heading - current_heading) % 360
    clockwise_rotation = (current_heading - desired_heading) % 360

    if clockwise_rotation <= counterclockwise_rotation:
        return ('CW: ',clockwise_rotation)
    else:
        return ('CCW: ',counterclockwise_rotation)

def draw_soccer_field():
    # Field dimensions
    field_length = 400
    field_width = 400

    # Goal area dimensions
    goal_width = 300
    goal_depth = 50

    # Center circle dimensions
    center_circle_radius = 50

    # Plot field lines
    plt.plot([-field_length/2, field_length/2], [-field_width/2, -field_width/2], 'w-', linewidth=2)  # Bottom boundary

    plt.plot([-field_length/2, field_length/2], [field_width/2, field_width/2], 'w-', linewidth=2)  # Top boundary

    plt.plot([field_length/2, field_length/2], [-field_width/2, field_width/2], 'w-', linewidth=2)  # Right boundary

    plt.plot([-field_length/2, -field_length/2], [-field_width/2, field_width/2], 'w-', linewidth=2)  # Left boundary

    plt.plot([-field_length/8, field_length/8], [-goal_width/2, -goal_width/2], 'w-', linewidth=2)  # Bottom goal line

    plt.plot([-field_length/8, field_length/8], [goal_width/2, goal_width/2], 'w-', linewidth=2)  # Top goal line

    plt.plot([field_length/8, field_length/8], [field_length/2, field_length/2-goal_depth], 'w-', linewidth=2)  # Top goal right line

    plt.plot([-field_length/8, -field_length/8], [field_length/2, field_length/2-goal_depth], 'w-', linewidth=2)  # Top goal left line

    plt.plot([field_length/8, field_length/8], [-field_length/2, -field_length/2+goal_depth], 'w-', linewidth=2)  # Bottom goal right line

    plt.plot([-field_length/8, -field_length/8], [-field_length/2, -field_length/2+goal_depth], 'w-', linewidth=2)  # Bottom goal left line

    # Plot center circle
    center_circle = plt.Circle((0, 0), center_circle_radius, color='white', linewidth=2, fill=False)
    plt.gca().add_artist(center_circle)

def calculate_angle_to_next_point(current_x, current_y, next_x, next_y):
    angle_to_next_point = np.degrees(np.arctan2(next_y - current_y, next_x - current_x))
    angle_to_next_point+=360
    angle_to_next_point = angle_to_next_point % 360
    return angle_to_next_point

def main():
    # Input robot position and heading here
    robot_x = 120 #set value for example
    robot_y = 150 #set value for example
    robot_heading = 240 #set value for example

    # Input ball position here
    ball_x = -90 #set value for example
    ball_y = -80 #set value for example

    # Create Node objects for robot and ball
    robot = Node(robot_x, robot_y)
    ball = Node(ball_x, ball_y)

    path = astar(robot, ball) #create path

    angle_to_next_point = calculate_angle_to_next_point(robot.x, robot.y, path[1][0],path[1][1]) #determine required rotation for next command

    # Determine whether left or right rotation is needed
    rotation_direction = calculate_rotation(robot_heading, angle_to_next_point)

    print("Rotation needed:", rotation_direction)

    if path:
        print("Path found:", path)
        path_x = [point[0] for point in path]
        path_y = [point[1] for point in path]

        plt.plot(path_x, path_y, '-k', linewidth=1)  # Black path
        plt.scatter(robot.x, robot.y, color='blue', s=200, label='Robot')  # Marker for robot
        plt.scatter(ball.x, ball.y, color='orange', label='Ball')  # Orange ball

        # Plotting robot heading
        arrow_length = 8
        dx = arrow_length * np.cos(np.deg2rad(robot_heading))
        dy = arrow_length * np.sin(np.deg2rad(robot_heading))
        plt.arrow(robot.x, robot.y, dx, dy, color='white', head_width=2, head_length=2)  # White arrow for heading

        draw_soccer_field()  # Draw soccer field layout

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Robot Path Planning')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.gcf().set_facecolor('white')
        plt.gca().set_facecolor('green')

        plt.show()
    else:
        print("No path found")

if __name__ == "__main__":
    main()
