import json
import time
import heapq

def closest_neighbor_heap(file_path):
    """
    This function implements the closest neighbor algorithm using a priority queue (heap) to find the shortest path
    in a graph.
    """
    def closest_neighbor(graph, start_vertex):
        """
        This nested function finds the shortest path using the closest neighbor algorithm.
        """
        start_time = time.time()  # Record the start time
        visited = set()
        visited.add(start_vertex)
        heap = []  # Priority queue to store unvisited vertices
        total_distance = 0
        iterations = 0

        # Add neighbors of the start vertex to the priority queue
        for neighbor, distance in graph[start_vertex].items():
            heapq.heappush(heap, (distance, start_vertex, neighbor))

        while heap:
            iterations += 1
            distance, src, current_vertex = heapq.heappop(heap)
            if current_vertex not in visited:
                total_distance += distance
                visited.add(current_vertex)
                # Add unvisited neighbors of the current vertex to the priority queue
                for neighbor, distance in graph[current_vertex].items():
                    if neighbor not in visited:
                        heapq.heappush(heap, (distance, current_vertex, neighbor))
                    
        end_time = time.time()  # Record the end time
        time_spent = end_time - start_time
        return time_spent, iterations, total_distance

    # Load JSON data from the provided file path
    with open(file_path, 'r') as file:
        graph = json.load(file)

    # Choose start vertex with the highest number of edges
    if lambda x: len(graph[x]):
        start_vertex = max(graph, key=lambda x: len(graph[x]))
    else:
        return 0, 0, 0
    # Run the algorithm
    time_spent, iterations, total_distance = closest_neighbor(graph, start_vertex)
    return time_spent, iterations, total_distance
