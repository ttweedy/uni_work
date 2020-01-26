import math
import os
import sys
import struct
from src.Direction import Direction

import random
from src.Route import Route

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification, first_pass):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random
        self.first_pass = first_pass
        self.last_dir = None
        self.thisMap = {}

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        route = Route(self.start)
        if self.first_pass:
            while self.current_position != self.end:
                self.get_next_random(route)
            return route

        else:
            while self.current_position != self.end:
                self.get_next(route)
            return route

    def get_next_random(self, route):
        cur_pos = (self.current_position.x, self.current_position.y)

        if self.thisMap.get(cur_pos) is None:
            self.thisMap[cur_pos] = 1
        else:
            amount = self.thisMap[cur_pos]
            amount += 1
            self.thisMap[cur_pos] = amount
        pos_directions = self.maze.get_possible_directions(self.current_position)
        map_list = [] #list of times ant has been to a coordinate
        dir_list = [] #list of minimum directions
        for n in pos_directions:
            # random.randint(0, pos_directions.size)
            next_pos = (self.current_position.add_direction(n).x, self.current_position.add_direction(n).y)
            if self.thisMap.get(next_pos) is None:
                self.thisMap[next_pos] = 0
            if len(map_list) == 0:
                map_list.append(self.thisMap[next_pos])
                dir_list.append(n)
            if self.thisMap[next_pos] <= min(map_list):
                map_list.append(self.thisMap[next_pos])
                dir_list.append(n)
        # next_direction = dir_list[random.randint(0, dir_list.count(Direction))]
        if map_list.count(map_list[0]) == len(map_list):
            next_direction = random.choice(dir_list)

        else:
            next_direction = dir_list[-1]



        self.current_position = self.current_position.add_direction(next_direction)
        # print(self.current_position)
        self.last_dir = next_direction
        # print(cur_pos)
        route.add(next_direction)

        return

    def get_next(self, route):
        possible_dir = self.maze.get_possible_directions(self.current_position)
        surrounding_pheromone = self.maze.get_surrounding_pheromone(self.current_position)
        total_pheromone = surrounding_pheromone.get_total_surrounding_pheromone()
        attractiveness = dict()

        attractiveness[Direction.north] = surrounding_pheromone.get(Direction.north)
        attractiveness[Direction.east] = surrounding_pheromone.get(Direction.east)
        attractiveness[Direction.south] = surrounding_pheromone.get(Direction.south)
        attractiveness[Direction.west] = surrounding_pheromone.get(Direction.west)

        if self.last_dir == Direction.north:
            total_pheromone = total_pheromone - attractiveness[Direction.south]
            attractiveness[Direction.south] = 0
        elif self.last_dir == Direction.south:
            total_pheromone = total_pheromone - attractiveness[Direction.north]
            attractiveness[Direction.north] = 0
        elif self.last_dir == Direction.east:
            total_pheromone = total_pheromone - attractiveness[Direction.west]
            attractiveness[Direction.west] = 0
        elif self.last_dir == Direction.west:
            total_pheromone = total_pheromone - attractiveness[Direction.east]
            attractiveness[Direction.east] = 0
        border_val = 500
        if self.thisMap.get(self.current_position.x, self.current_position.y + 1) > border_val:
            attractiveness[Direction.north] = 0
        if self.thisMap.get(self.current_position.x + 1, self.current_position.y) > border_val:
            attractiveness[Direction.east] = 0
        if self.thisMap.get(self.current_position.x - 1, self.current_position.y) > border_val:
            attractiveness[Direction.west] = 0
        if self.thisMap.get(self.current_position.x, self.current_position.y - 1) > border_val:
            attractiveness[Direction.south] = 0

        if attractiveness[Direction.north] + attractiveness[Direction.south] + attractiveness[Direction.east] + \
                attractiveness[Direction.west] == 0:
            self.get_next_random(route)
            return

        if total_pheromone == 0:
            for dir in attractiveness:
                attractiveness[dir] = self.next_up(attractiveness[dir])
            total_pheromone = self.next_up(total_pheromone)

        randint = self.rand.random()
        cumulative = 0

        for dir in possible_dir:
            weight = attractiveness[dir] / total_pheromone
            if randint <= weight + cumulative:
                if self.maze.in_bounds(self.current_position.add_direction(dir)):
                    self.current_position = self.current_position.add_direction(dir)
                    self.last_dir = dir
                    route.add(dir)
                    cur_pos = (self.current_position.x, self.current_position.y)
                    if self.thisMap.get(cur_pos) is None:
                        self.thisMap[cur_pos] = 1
                        # print(self.thisMap)
                    else:
                        amount = self.thisMap[cur_pos]
                        amount += 1
                        self.thisMap[cur_pos] = amount
                        #print(self.thisMap)
                        # map (coordinate, amount of times travelled past)
                return
            cumulative = cumulative + weight

    # src: https://stackoverflow.com/questions/10420848/how-do-you-get-the-next-value-in-the-floating-point-sequence/
    # 10426033#10426033
    @staticmethod
    def next_up(x):
        # NaNs and positive infinity map to themselves.
        if math.isnan(x) or (math.isinf(x) and x > 0):
            return x

        # 0.0 and -0.0 both map to the smallest +ve float.
        # if x == 0.0:
        #    x = 0.0

        n = struct.unpack('<q', struct.pack('<d', x))[0]
        if n >= 0:
            n += 1
        else:
            n -= 1
        return struct.unpack('<d', struct.pack('<q', n))[0]
