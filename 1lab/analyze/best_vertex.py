import json
import time
from tkinter import filedialog

def closest_neighbor(graph, start_vertex):
    """
    Finds the closest neighbor in a graph starting from a specified vertex.
    """
    start_time = time.time()  # Record the start time
    visited = set()
    current_vertex = start_vertex
    visited.add(current_vertex)
    total_weight = 0  # Initialize total weight counter
    iterations = 0  # Initialize iterations counter
    
    while len(visited) < len(graph):
        min_distance = float('inf')
        closest_vertex = None
        
        for neighbor, distance in graph[current_vertex].items():
            if neighbor not in visited and distance < min_distance:
                min_distance = distance
                closest_vertex = neighbor
        
        if closest_vertex is None:
            break

        total_weight += min_distance  # Update total weight
        current_vertex = closest_vertex
        visited.add(current_vertex)
        iterations += 1  # Increment iterations counter
    
    end_time = time.time()  # Record the end time
    time_spent = end_time - start_time
    return time_spent, iterations, total_weight

def closest_neighbor_vertex_choose(file_path):
    """
    Chooses the start vertex with the highest number of edges and runs the closest neighbor algorithm.
    """
    # Load JSON data from the specified file path
    with open(file_path, 'r') as file:
        graph = json.load(file)

    # Choose start vertex with the highest number of edges
    start_vertex = max(graph, key=lambda x: len(graph[x]))

    # Run the algorithm and retrieve results
    return closest_neighbor(graph, start_vertex)

# Test function
def test_closest_neighbor_vertex_choose():
    """
    Tests the closest_neighbor_vertex_choose function with a sample graph.
    """
    # Define a sample graph in JSON format
    sample_graph = {
        'A': {'B': 2, 'C': 3},
        'B': {'A': 2, 'C': 4},
        'C': {'A': 3, 'B': 4}
    }
    
    # Call the function with the sample graph
    time_spent, iterations, total_weight = closest_neighbor(sample_graph, 'A')
    
    # Print the results
    print("Time Spent:", time_spent)
    print("Iterations:", iterations)
    print("Total Weight:", total_weight)
