import os
import sys
from multiprocessing.pool import ThreadPool as Pool

from src.Ant import Ant

import time
from src.Maze import Maze
from src.PathSpecification import PathSpecification

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation

    # Loop that starts the shortest path process
    # @param spec Specification of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        self.maze.reset()
        s = None
        route_lens = []
        # pool = Pool(16)
        for x in range(0, self.generations):
            global routes
            routes = []
            for y in range(0, self.ants_per_gen):
                first_pass = False
                if x == 0:
                    first_pass = True
                # pool.apply(self.process_ant, [first_pass, path_specification, routes])
                self.process_ant(first_pass,path_specification, routes)
            self.maze.add_pheromone_routes(routes, self.q)
            self.maze.evaporate(self.evaporation)
            shortest = self.shortest_route(routes)
            if x == 0:
                s = shortest
            if shortest.size() < s.size():
                s = shortest
            route_lens.append(shortest.size())
            print(route_lens)
            print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))
        # pool.close()
        # .join()
        return s

    def process_ant(self, first_pass, path_specification, routes):
        ant = Ant(self.maze, path_specification, first_pass)
        route = ant.find_route()
        routes.append(route)
        return

    def shortest_route(self, routes):
        if len(routes) == 0:
            return
        shortest = routes[0]

        for r in routes:
            if r.shorter_than(shortest):
                shortest = r

        return shortest


# Driver function for Assignment 1
if __name__ == "__main__":
    # parameters
    gen = 1
    no_gen = 5
    q = 5000
    evap = 0.4

    # construct the optimization objects
    maze = Maze.create_maze("./../data/hard maze.txt")
    spec = PathSpecification.read_coordinates("./../data/hard coordinates.txt")
    aco = AntColonyOptimization(maze, gen, no_gen, q, evap)
    # save starting time
    start_time = int(round(time.time() * 1000))
    # run optimization
    shortest_route = aco.find_shortest_route(spec)
    #print(shortest_route)
    # print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))
    # save solution
<<<<<<< HEAD
    shortest_route.write_to_file("./../data/hard_solution.txt")
=======
    shortest_route.write_to_file("./../data/easy_solution.txt")
>>>>>>> rewrite-ACO

    # print route size
    # print("Route size: " + str(shortest_route.size()))
