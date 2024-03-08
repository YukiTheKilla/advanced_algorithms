import json
import random
import time

def mmas(file_path):
    """
    This function implements the Max-Min Ant System algorithm to find the shortest path in a graph.
    """
    with open(file_path, 'r') as file:
        graph = json.load(file)
        
    iterations = 10
    evaporation_rate = 0.5
    alpha = 1
    beta = 1
    min_pheromone = 0.1
    max_pheromone = 1
    
    ca_generator = ant_colony(graph, alpha, beta, evaporation_rate, iterations, min_pheromone, max_pheromone)

    global number
    global total_weight
    
    number = 0
    total_weight = 0
    
    start_time = time.time()
    
    for adjacency_list in ca_generator:
        graph_data = {vertex: edges for vertex, edges in adjacency_list.items() if edges}
        num_edges = len(graph_data)
        total_weight = sum(weight for edges in graph_data.values() for weight in edges.values())

        number += 1

    end_time = time.time()
    watch = end_time - start_time
    return watch, number, total_weight

def initialize_pheromone_levels(graph, max_pheromone):
    """
    Initialize pheromone levels for all edges in the graph.
    """
    pheromone_levels = {}
    for node in graph.keys():
        pheromone_levels[node] = {neighbor: max_pheromone for neighbor in graph[node]}
    return pheromone_levels

def generate_ant_path(graph, pheromone_levels, alpha, beta, start_node):
    """
    Generate a path for an ant based on the current pheromone levels and heuristic information.
    """
    ant_path = [start_node]
    current_node = start_node
    while len(ant_path) < len(graph):
        probabilities = []
        available_neighbors = [neighbor for neighbor in graph[current_node] if neighbor not in ant_path]
        if not available_neighbors:
            break
        pheromone_sum = sum(pheromone_levels[current_node][neighbor] ** alpha for neighbor in available_neighbors)
        for neighbor in available_neighbors:
            pheromone_level = pheromone_levels[current_node][neighbor]
            attractiveness = (pheromone_level ** alpha) * ((1 / graph[current_node][neighbor]) ** beta)
            probability = attractiveness / pheromone_sum
            probabilities.append((neighbor, probability))
        probabilities.sort(key=lambda x: x[1], reverse=True)
        selected_node = None
        probability_sum = 0
        random_value = random.random()
        for neighbor, probability in probabilities:
            probability_sum += probability
            if random_value <= probability_sum:
                selected_node = neighbor
                break
        if selected_node is None:
            selected_node = probabilities[0][0]
        ant_path.append(selected_node)
        current_node = selected_node
    return ant_path

def calculate_path_length(graph, path):
    """
    Calculate the total length of a given path in the graph.
    """
    length = 0
    for i in range(len(path) - 1):
        length += graph[path[i]][path[i + 1]]
    return length

def update_pheromone_levels(pheromone_levels, ant_path, path_length, evaporation_rate, min_pheromone, max_pheromone):
    """
    Update pheromone levels on edges based on the ants' paths, evaporation rate, and minimum/maximum pheromone values.
    """
    evaporation_amount = 1 - evaporation_rate
    for i in range(len(ant_path) - 1):
        current_node = ant_path[i]
        next_node = ant_path[i + 1]
        pheromone_levels[current_node][next_node] = max(min_pheromone, min((evaporation_amount * pheromone_levels[current_node][next_node]) + (1 / path_length), max_pheromone))

def ant_colony(graph, alpha, beta, evaporation_rate, iterations, min_pheromone, max_pheromone):
    """
    Implementation of the ant colony optimization algorithm with Max-Min Ant System.
    """
    start_node = random.choice(list(graph.keys()))
    pheromone_levels = initialize_pheromone_levels(graph, max_pheromone)
    best_path_length = float('inf')
    best_path = None
    for _ in range(iterations):
        ant_path = generate_ant_path(graph, pheromone_levels, alpha, beta, start_node)
        path_length = calculate_path_length(graph, ant_path)
        if path_length < best_path_length:
            best_path_length = path_length
            best_path = ant_path[:]
        update_pheromone_levels(pheromone_levels, ant_path, path_length, evaporation_rate, min_pheromone, max_pheromone)
        adjacency_list = {vertex: {} for vertex in graph}
        for i in range(len(ant_path) - 1):
            from_vertex = ant_path[i]
            to_vertex = ant_path[i + 1]
            edge_weight = graph[from_vertex][to_vertex]
            adjacency_list[from_vertex][to_vertex] = edge_weight
        yield adjacency_list
