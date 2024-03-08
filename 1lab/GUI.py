import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import math
import json
import random
import sys 

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
        
        self.optimal_path_button = tk.Button(self, text="Find Optimal Path", command=self.find_closest_neighbor_path)
        self.optimal_path_button.pack()
        
        self.graph_data = {}
        self.selected_vertices = []

        self.canvas.bind("<Button-1>", self.on_click)
        
    def find_closest_neighbor_path(self):
        self.clear_graph()
        def read_json_file():
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data

        graph = read_json_file()
        start = "V"+ str(random.randint(2,len(graph))-1)
        visited = [start]
        path = [start]
        current_node = start
        while len(visited) < len(graph):
            nearest_neighbor = None
            min_distance = float('inf')
            for neighbor, distance in graph[current_node].items():
                if neighbor not in visited:
                    if distance < min_distance:
                        min_distance = distance
                        nearest_neighbor = neighbor
            if nearest_neighbor is None:
                if start in graph[current_node]:
                    path.append(start)
                    break
                else:
                    break
            visited.append(nearest_neighbor)
            path.append(nearest_neighbor)
            current_node = nearest_neighbor

        # Create adjacency list for the path
        adjacency_list = {}
        for i in range(len(path) - 1):
            adjacency_list[path[i]] = {path[i + 1]: graph[path[i]][path[i + 1]]}

        self.graph_data = {vertex: edges for vertex, edges in adjacency_list.items() if edges}
        self.draw_graph()

    def draw_optimal_path(self, path):
        self.canvas.delete("optimal_path")
        for i in range(len(path) - 1):
            source = path[i]
            destination = path[i + 1]
            x1, y1 = self.graph_data[source]['x'], self.graph_data[source]['y']
            x2, y2 = self.graph_data[destination]['x'], self.graph_data[destination]['y']
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="green", width=2, tag="optimal_path")

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
