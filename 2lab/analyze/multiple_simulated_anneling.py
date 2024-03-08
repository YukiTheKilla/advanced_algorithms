import math
import json
import random
import time

def multiple_runs_simulated_annealing(file_path, num_runs=10):
    """
    This function performs multiple runs of the simulated annealing algorithm and returns the best solution found.
    """
    best_solution = None
    best_watch = float('inf')
    best_number = 0
    best_total_weight = 0
    
    for _ in range(num_runs):
        watch, number, total_weight = simulated_annealing(file_path)
        if watch < best_watch:
            best_watch = watch
            best_number = number
            best_total_weight = total_weight

    return best_watch, best_number, best_total_weight


def simulated_annealing(file_path):
    """
    This function implements the simulated annealing algorithm to find the shortest path in a graph.
    """
    with open(file_path, 'r') as file:
        graph = json.load(file)

    # Choose start vertex with at least one neighbor
    if graph:
        start_vertex = None
        for vertex in graph:
            if len(graph[vertex]) > 0:
                start_vertex = vertex
                break

    # Initialize parameters
    T = 100
    T_min = 1
    alpha = 0.5
    
    # Randomly adjust parameters within a small range
    T_fluid = T + (T * 0.01 * random.randint(-10, 10))
    T_min_fluid = T_min + (T_min * 0.01 * random.randint(-10, 10))
    alpha_fluid = alpha + (alpha * 0.01 * random.randint(10, 10))
    
    # Run the algorithm
    sa_generator = simulated_annealing_algorithm(graph, T_fluid, T_min_fluid, alpha_fluid)
    
    global number
    global total_weight
    
    number = 0
    total_weight = 0
    
    start_time = time.time()
    
    # Iterate over the generator to perform the algorithm
    for adjacency_list in sa_generator:
        graph_data = {vertex: edges for vertex, edges in adjacency_list.items() if edges}
        num_edges = len(graph_data)
        total_weight = sum(weight for edges in graph_data.values() for weight in edges.values())
        number += 1
    
    end_time = time.time()
    watch = end_time - start_time
    return watch, number, total_weight


def simulated_annealing_algorithm(graph, T, T_min, alpha):
    """
    This function implements the simulated annealing algorithm.
    """
    def energy(solution):
        """
        Calculate the energy (total distance) of a solution.
        """
        total_distance = 0
        if len(solution) < 2:
            return total_distance  # Return 0 if solution has less than 2 elements
        for i in range(len(solution) - 1):
            if solution[i + 1] in graph[solution[i]]:
                total_distance += graph[solution[i]][solution[i + 1]]
        if solution[1] in graph[solution[-1]] and solution[0] in graph[solution[-1]]:
            total_distance += graph[solution[-1]][solution[0]]
        return total_distance

    def neighbor_solution(current_solution):
        """
        Generate a neighboring solution based on the current solution.
        """
        new_solution = current_solution[:]
        operation = random.choice(['swap', 'reverse', 'shift'])

        if operation == 'swap':
            i, j = random.sample(range(len(new_solution)), 2)
            while i == j:
                j = random.randint(0, len(new_solution) - 1)
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        elif operation == 'reverse':
            i, j = sorted(random.sample(range(len(new_solution)), 2))
            new_solution[i:j+1] = reversed(new_solution[i:j+1])
        elif operation == 'shift':
            i, j = sorted(random.sample(range(len(new_solution)), 2))
            new_solution = new_solution[:i] + new_solution[j:i-1:-1] + new_solution[j+1:]

        # Check if the new solution maintains all vertices in the graph
        if all(vertex in new_solution for vertex in graph):
            return new_solution
        else:
            # If the new solution is invalid, return the original solution
            return current_solution

    # Initialize current solution
    current_solution = list(graph.keys())
    random.shuffle(current_solution)

    # Simulated annealing loop
    while T > T_min:
        new_solution = neighbor_solution(current_solution)
        delta_E = energy(new_solution) - energy(current_solution)
        if delta_E < 0:
            current_solution = new_solution
        elif random.random() < math.exp(-delta_E / T):
            current_solution = new_solution
        T = T * alpha

        # Generate adjacency list for the current solution
        adjacency_list = {}
        for i in range(len(current_solution) - 1):
            if current_solution[i] not in adjacency_list:
                adjacency_list[current_solution[i]] = {}
            if current_solution[i + 1] in graph[current_solution[i]]:
                adjacency_list[current_solution[i]][current_solution[i + 1]] = graph[current_solution[i]][current_solution[i + 1]]

        # Check the edge from the last vertex to the first
        if current_solution[-1] not in adjacency_list:
            adjacency_list[current_solution[-1]] = {}
        if current_solution[0] in graph[current_solution[-1]]:
            adjacency_list[current_solution[-1]][current_solution[0]] = graph[current_solution[-1]][current_solution[0]]

        yield adjacency_list
