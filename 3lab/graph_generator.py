import os
import tkinter as tk
from tkinter import ttk
import json
import random
import tkinter.messagebox

class GraphRandomizer(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

        # Variables for user input
        self.min_vertices = tk.IntVar(value=10)
        self.max_vertices = tk.IntVar(value=200)
        self.edge_probability = tk.DoubleVar(value=0.5)
        self.weight_range = tk.StringVar(value="1-10")
        self.shift = tk.IntVar(value=1)

        # Set up UI
        ttk.Label(self, text="Minimum Vertices(min 10-40):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self, textvariable=self.min_vertices).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Maximum Vertices:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self, textvariable=self.max_vertices).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Edge Probability (0-1):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self, textvariable=self.edge_probability).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Weight Range (min-max):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self, textvariable=self.weight_range).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Shift:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self, textvariable=self.shift).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self, text="Generate Graphs", command=self.generate_graphs).grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def generate_graphs(self):
        min_vertices = self.min_vertices.get()
        max_vertices = self.max_vertices.get()
        edge_probability = self.edge_probability.get()
        weight_min, weight_max = map(int, self.weight_range.get().split('-'))
        shift = self.shift.get()
        
        for num_vertices in range(min_vertices, max_vertices + 1, shift):
            graph = {}
            for i in range(1, num_vertices + 1):
                connections = {}
                for j in range(1, num_vertices + 1):
                    if i != j and random.random() <= edge_probability:
                        connections[f"V{j}"] = random.randint(weight_min, weight_max)
                if connections:
                    graph[f"V{i}"] = connections

            directory = "randomized"
            os.makedirs(directory, exist_ok=True)
            filename = f"{directory}/random_graph_{num_vertices}_vertices.json"
            with open(filename, "w") as f:
                json.dump(graph, f, indent=4)

        tkinter.messagebox.showinfo("Success", f"Graphs generated and saved to 'randomized' directory")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphRandomizer(root)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
