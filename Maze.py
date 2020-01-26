import os
import sys
import traceback
from src.Direction import Direction
from src.SurroundingPheromone import SurroundingPheromone

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.pheromones = self.initialize_pheromones()

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        pheromones = [[0 for x in range(self.length)] for y in range(self.width)]
        return pheromones

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        if route.size() <= 0:
            return
        pheromone_value = q / route.size()
        current_pos = route.get_start()
        current_pheromone = self.pheromones[current_pos.get_x()][current_pos.get_y()]
        self.pheromones[current_pos.get_x()][current_pos.get_y()] = current_pheromone + pheromone_value
        for direction in route.get_route():
            current_pos = current_pos.add_direction(direction)
            current_pheromone = self.pheromones[current_pos.get_x()][current_pos.get_y()]
            self.pheromones[current_pos.get_x()][current_pos.get_y()] = current_pheromone + pheromone_value
        return

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        for x in range(self.width):
            for y in range(self.length):
                self.pheromones[x][y] = self.pheromones[x][y] * rho
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    def get_possible_directions(self, pos):
        directions = []
        north = pos.add_direction(Direction.north)
        east = pos.add_direction(Direction.east)
        south = pos.add_direction(Direction.south)
        west = pos.add_direction(Direction.west)
        if self.in_bounds(north) and self.walls[north.get_x()][north.get_y()] == 1:
            directions.append(Direction.north)
        if self.in_bounds(east) and self.walls[east.get_x()][east.get_y()] == 1:
            directions.append(Direction.east)
        if self.in_bounds(south) and self.walls[south.get_x()][south.get_y()] == 1:
            directions.append(Direction.south)
        if self.in_bounds(west) and self.walls[west.get_x()][west.get_y()] == 1:
            directions.append(Direction.west)

        return directions

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        north = 0
        east = 0
        south = 0
        west = 0
        if self.in_bounds(position.add_direction(Direction.north)):
            north = self.get_pheromone(position.add_direction(Direction.north))
        if self.in_bounds(position.add_direction(Direction.east)):
            east = self.get_pheromone(position.add_direction(Direction.east))
        if self.in_bounds(position.add_direction(Direction.south)):
            south = self.get_pheromone(position.add_direction(Direction.south))
        if self.in_bounds(position.add_direction(Direction.west)):
            west = self.get_pheromone(position.add_direction(Direction.west))

        return SurroundingPheromone(north, east, south, west)

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        return self.pheromones[pos.get_x()][pos.get_y()]

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])
            
            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])
            
            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
