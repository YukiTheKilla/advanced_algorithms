import tkinter as tk
from tkinter import filedialog, simpledialog, Entry, Label
import math
import json
import random
import sys 
import time

class GraphVisualization(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.canvas = tk.Canvas(self, bg="white", width=600, height=400)
        self.canvas.pack(expand=True, fill=tk.BOTH,side=tk.RIGHT)
        
        self.save_button = tk.Button(self, text="Save Handmade", command=self.save_json)
        self.save_button.pack()
        
        self.clear_button = tk.Button(self, text="Clear Graph", command=self.clear_graph)
        self.clear_button.pack()
        
        self.load_button = tk.Button(self, text="Load JSON", command=self.load_json)
        self.load_button.pack()
        
        self.optimal_path_button = tk.Button(self, text="Find Optimal Path", command=self.algorithm_func)
        self.optimal_path_button.pack()
        
        self.T_label = Label(self, text="Temperature (T):")
        self.T_label.pack()
        self.T_entry = Entry(self)
        self.T_entry.insert(tk.END, "100")
        self.T_entry.pack()
        
        self.T_min_label = Label(self, text="Minimum Temperature (T_min):")
        self.T_min_label.pack()
        self.T_min_entry = Entry(self)
        self.T_min_entry.insert(tk.END, "1")
        self.T_min_entry.pack()
    
        self.alpha_label = Label(self, text="Alpha (a):")
        self.alpha_label.pack()
        self.alpha_entry = Entry(self)
        self.alpha_entry.insert(tk.END, "0.95")
        self.alpha_entry.pack()
        
        self.graph_data = {}
        self.selected_vertices = []

        self.canvas.bind("<Button-1>", self.on_click)
            
    def algorithm_func(self):
        self.clear_graph()
        def read_json_file():
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data

        graph = read_json_file()
        T = float(self.T_entry.get())
        T_min = float(self.T_min_entry.get())
        alpha = float(self.alpha_entry.get())

        def simulated_annealing(graph, T, T_min, alpha):
            def energy(solution):
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
                def is_valid_solution(solution, graph):
                    """
                    Check if the solution maintains all vertices in the graph.
                    """
                    # Get all vertices in the graph
                    all_vertices = set(graph.keys())
                    
                    # Check if all vertices in the solution are present in the graph
                    solution_vertices = set(solution)
                    valid = all_vertices == solution_vertices
                    
                    return valid
                # Check validity of the new solution
                if is_valid_solution(new_solution,graph):
                    return new_solution
                else:
                    # If the new solution is invalid, return the original solution
                    return current_solution

            current_solution = list(graph.keys())
            random.shuffle(current_solution)

            while T > T_min:
                new_solution = neighbor_solution(current_solution)
                delta_E = energy(new_solution) - energy(current_solution)
                if delta_E < 0:
                    current_solution = new_solution
                elif random.random() < math.exp(-delta_E / T):
                    current_solution = new_solution
                T = T * alpha

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

        # Получаем генератор для алгоритма отжига
        sa_generator = simulated_annealing(graph, T, T_min, alpha)
        
        global number
        
        number = 0

        start_time = time.time()
        for adjacency_list in sa_generator:
            self.graph_data = {vertex: edges for vertex, edges in adjacency_list.items() if edges}
            num_edges = len(self.graph_data)
            total_weight = sum(weight for edges in self.graph_data.values() for weight in edges.values())

            number += 1
            print(f"{number}. Количество путей: {num_edges}  Общий вес: {total_weight}")
        
        end_time = time.time()
        watch = end_time - start_time
        print(f"Время: {watch:.5f}")
        self.draw_graph()

    def clear_graph(self):
        self.canvas.delete("all")
        self.graph_data.clear()
        
    def on_click(self, event):
        x, y = event.x, event.y
        clicked_vertex = self.find_vertex(x, y)
        if clicked_vertex:
            self.toggle_vertex_selection(clicked_vertex)
            if len(self.selected_vertices) == 2:
                self.add_edge(*self.selected_vertices)
                self.prompt_edge_weight(*self.selected_vertices)
                self.selected_vertices = []
        else:
            vertex_name = f"V{len(self.graph_data) + 1}"
            self.graph_data[vertex_name] = {'x': x, 'y': y}
            self.draw_vertex(x, y, vertex_name)

    def prompt_edge_weight(self, source, destination):
        weight = simpledialog.askinteger("Edge Weight", f"Enter the weight of edge {source}-{destination}")
        if weight is not None:
            self.graph_data[(source, destination)] = {'weight': weight}
            self.add_edge(source, destination, weight)

    def find_vertex(self, x, y):
        for vertex_name, vertex_data in self.graph_data.items():
            vx, vy = vertex_data['x'], vertex_data['y']
            if (x - 5) <= vx <= (x + 5) and (y - 5) <= vy <= (y + 5):
                return vertex_name
        return None

    def toggle_vertex_selection(self, vertex_name):
        if vertex_name in self.selected_vertices:
            self.selected_vertices.remove(vertex_name)
        else:
            self.selected_vertices.append(vertex_name)

    def draw_vertex(self, x, y, vertex_name):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", outline="black")
        self.canvas.create_text(x, y - 10, text=vertex_name)

    def add_edge(self, source, destination, weight=None):
        x1, y1 = self.graph_data[source]['x'], self.graph_data[source]['y']
        x2, y2 = self.graph_data[destination]['x'], self.graph_data[destination]['y']
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=1)
        if weight is not None:
            text_x = x2 - 10 if x1 < x2 else x2 + 10
            text_y = y2 - 10 if y1 < y2 else y2 + 10
            self.canvas.create_text(text_x, text_y, text=str(weight), fill="red",width = 0, tag="weight",font=("Arial", 10, "bold"), anchor=tk.CENTER)

    def load_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as f:
                loaded_data = json.load(f)
            self.graph_data = {vertex: edges for vertex, edges in loaded_data.items() if edges}
            self.draw_graph()

    def draw_graph(self):
        all_vertices = self.get_all_vertices(self.graph_data)
        num_vertices = len(all_vertices)
        
        center_x = 300
        center_y = 200
        radius = min(150, min(center_x, center_y) - 50)

        angle_increment = 2 * math.pi / num_vertices
        current_angle = 0

        vertex_positions = {}
        for vertex in all_vertices:
            x = center_x + radius * math.cos(current_angle)
            y = center_y + radius * math.sin(current_angle)
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", outline="black")
            self.canvas.create_text(x, y - 10, text=vertex)
            vertex_positions[vertex] = (x, y)
            current_angle += angle_increment

        for vertex, edges in self.graph_data.items():
            x1, y1 = vertex_positions[vertex]
            for destination, weight in edges.items():
                x2, y2 = vertex_positions[destination]
                arrow_line = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2, tag="edge")
                text_x = x2 - 10 if x1 < x2 else x2 + 10
                text_y = y2 - 10 if y1 < y2 else y2 + 10
                self.canvas.create_text(text_x, text_y, text=str(weight), fill="red", tag="weight", anchor=tk.CENTER)

    def get_all_vertices(self, graph):
        all_vertices = set(graph.keys())
        for edges in graph.values():
            for vertex in edges.keys():
                all_vertices.add(vertex)
        return all_vertices
    
    def save_json(self, filename=None):
        if not filename:
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        # Prepare adjacency list
        adjacency_list = {}
        for (source, destination), data in self.graph_data.items():
            if source not in adjacency_list:
                adjacency_list[source] = {}
            if 'weight' in data:
                adjacency_list[source][destination] = data['weight']
        # Write adjacency list to JSON file
        if filename:
            with open(filename, "w") as f:
                json.dump(adjacency_list, f)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI")
    root.geometry("800x600")

    # Create an instance of GraphVisualization
    graph_visualization = GraphVisualization(root)
    graph_visualization.pack(expand=True, fill=tk.BOTH)

    # Function to terminate the process
    def on_closing():
        root.destroy()
        sys.exit()

    # Bind the closing event of the window to the function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
