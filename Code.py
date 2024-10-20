import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix

# adjacency matrix
adj_matrix = np.array([
    [0, 51, 0, 0, 0, 0, 302, 0, 0, 0],   # Dongguan (0)
    [51, 0, 19, 0, 0, 117, 0, 0, 0, 0],  # Guangzhou (1)
    [0, 19, 0, 62, 50, 0, 0, 0, 0, 0],   # Foshan (2)
    [0, 0, 62, 0, 32, 0, 0, 0, 69, 342], # Zhongshan (3)
    [0, 0, 50, 32, 0, 0, 0, 0, 0, 0],    # Jiangmen (4)
    [0, 117, 0, 0, 0, 0, 0, 0, 73, 0],   # Huizhou (5)
    [302, 0, 0, 0, 0, 0, 0, 0, 283, 0],  # Shantou (6)
    [0, 0, 0, 69, 0, 0, 0, 0, 58, 350],  # Zhuhai (7)
    [0, 0, 0, 69, 0, 73, 283, 58, 0, 0], # Shenzhen (8)
    [0, 0, 0, 342, 0, 0, 0, 350, 0, 0]   # Zhanjiang (9)
])

graph = csr_matrix(adj_matrix)

# Dijkstra algorithm
dist_matrix, predecessors = dijkstra(csgraph=graph, return_predecessors=True)

# Dictionary to convert into city name for the query 
city_names = {
    0: "Dongguan",
    1: "Guangzhou",
    2: "Foshan",
    3: "Zhongshan",
    4: "Jiangmen",
    5: "Huizhou",
    6: "Shantou",
    7: "Zhuhai",
    8: "Shenzhen",
    9: "Zhanjiang"
}

# Shortest paths
def get_path(predecessors, start, end):
    path = []
    i = end
    while i != start:
        path.append(i)
        i = predecessors[start, i]
        if i == -9999:
            return "No path"
    path.append(start)
    return path[::-1]

# Queries to search
queries = {
    "Shenzhen to Guangzhou": (8, 1),
    "Huizhou to Zhanjiang": (5, 9),
    "Shantou to Jiangmen": (6, 4),
    "Dongguan to Zhanjiang": (0, 9)
}

# Results
results = {}
for query, (start, end) in queries.items():
    path = get_path(predecessors, start, end)
    if path == "No path":
        results[query] = {"path": path, "distance": "Infinity"}
        continue
    
    path_names = [city_names[city] for city in path]  # Converting indexes into names
    total_distance = 0
    steps_with_distances = []

    # Calculate cumulative distances for each stage
    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]
        step_distance = adj_matrix[from_city, to_city]
        total_distance += step_distance
        steps_with_distances.append(f"{city_names[from_city]} -> {city_names[to_city]} ({step_distance} km)")

    results[query] = {"path": steps_with_distances, "distance": total_distance}

# print results with cumulative distances
for query, result in results.items():
    print(f"Query: {query}")
    if result['path'] == "No path":
        print(f"No path available")
    else:
        for step in result['path']:
            print(step)
        print(f"Total distance: {result['distance']} km\n")
