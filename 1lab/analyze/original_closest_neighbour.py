import json
import random
import time

def find_closest_neighbor(graph, start_vertex):
    """
    Finds the closest neighbor to each vertex in the graph, starting from the given start_vertex.
    """
    start_time = time.time()  # Record the start time
    visited = set()
    current_vertex = start_vertex
    visited.add(current_vertex)
    total_weight = 0
    iterations = 0
    
    while len(visited) < len(graph):
        min_distance = float('inf')
        closest_vertex = None
        
        # Find the closest unvisited neighbor
        for neighbor, distance in graph[current_vertex].items():
            if neighbor not in visited and distance < min_distance:
                min_distance = distance
                closest_vertex = neighbor
        
        if closest_vertex:
            # Move to the closest neighbor
            current_vertex = closest_vertex
            visited.add(current_vertex)
            total_weight += min_distance
            iterations += 1
        else:
            break
    
    end_time = time.time()  # Record the end time
    time_spent = end_time - start_time
    return time_spent, iterations, total_weight

def closest_neighbor(file_path):
    """
    Finds the closest neighbor using the provided graph data in the given file.
    """
    # Load JSON data from the provided file path
    with open(file_path, 'r') as file:
        graph = json.load(file)

    # Choose start vertex randomly if graph is not empty
    if graph:
        start_vertex = random.choice(list(graph.keys()))
    else:
        return 0, 0, 0

    # Run the algorithm
    time_spent, iterations, total_weight = find_closest_neighbor(graph, start_vertex)
    return time_spent, iterations, total_weight
