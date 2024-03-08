import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import json
import time
from original_closest_neighbour import closest_neighbor as original_func
from heap_vertex_store import closest_neighbor_heap as heap_store_func
from best_vertex import closest_neighbor_vertex_choose as vertex_choose_func

# Define your functions
def original_func_wrapper(file_path):
    start_time = time.time()
    _, _, total_weight = original_func(file_path)
    end_time = time.time()
    time_spent = end_time - start_time
    return time_spent, total_weight

def heap_store_func_wrapper(file_path):
    start_time = time.time()
    _, _, total_weight = heap_store_func(file_path)
    end_time = time.time()
    time_spent = end_time - start_time
    return time_spent, total_weight

def vertex_choose_func_wrapper(file_path):
    start_time = time.time()
    _, _, total_weight = vertex_choose_func(file_path)
    end_time = time.time()
    time_spent = end_time - start_time
    return time_spent, total_weight

# Create the GUI
def create_gui():
    def choose_files():
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            execute_button.config(state=tk.NORMAL)
            file_label.config(text=f"Selected Files: {', '.join(file_paths)}")
            execute_button.config(command=lambda: execute_functions(file_paths))

    def execute_functions(file_paths):
        num_vertices_list = []
        times_list = [[] for _ in range(3)]
        total_weights_list = [[] for _ in range(3)]
        
        for file_path in file_paths:
            with open(file_path, "r") as f:
                data = json.load(f)
            num_vertices = len(data)
            num_vertices_list.append(num_vertices)

            for i, func in enumerate([original_func_wrapper, heap_store_func_wrapper, vertex_choose_func_wrapper]):
                time_spent, total_weight = func(file_path)
                times_list[i].append(time_spent)
                total_weights_list[i].append(total_weight)

        plot_graph(num_vertices_list, times_list, "Time Spent (seconds)", "Time Spent per Function")
        plot_graph(num_vertices_list, total_weights_list, "Total Weight", "Total Weight per Function")

    def plot_graph(x_data, y_data, ylabel, title):
        plt.figure()
        function_names = ["Closest Neighbour(CN)", "Heap Store(CN)", "Best Vertex(CN)"]
        for i, func_data in enumerate(y_data):
            plt.plot(x_data, func_data, label=function_names[i], marker='o', markersize=1, linestyle='-')
        plt.xlabel('Number of Vertices')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()

        # Set round edges for all elements
        for spine in plt.gca().spines.values():
            spine.set_edgecolor('black')  # Set the edge color to black
            spine.set_linewidth(1.5)      # Set the width of the edges
            spine.set_capstyle('round')   # Set round edges

        # Set round edges for ticks
        plt.tick_params(axis='both', width=2, length=6, direction='inout', pad=10)
        plt.gca().tick_params(width=2, length=6, direction='inout', pad=10)

        plt.show()


    root = tk.Tk()
    root.title("Function GUI")

    # Choose Files button
    choose_button = tk.Button(root, text="Choose Files", command=choose_files)
    choose_button.pack()

    # Label to display selected files
    file_label = tk.Label(root, text="Selected Files: ")
    file_label.pack()

    # Execute button (initially disabled)
    execute_button = tk.Button(root, text="Execute", state=tk.DISABLED)
    execute_button.pack()

    root.mainloop()

# Call the function to create the GUI
create_gui()
