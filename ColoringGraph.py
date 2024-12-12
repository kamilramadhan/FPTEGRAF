import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from random import choice

regions = {
    "Surabaya Pusat": (0.5, 0.5),
    "Surabaya Timur": (0.8, 0.5),
    "Surabaya Barat": (0.2, 0.5),
    "Surabaya Utara": (0.5, 0.8),
    "Surabaya Selatan": (0.5, 0.2),
    "Tunjungan Plaza": (0.6, 0.6),
    "Darmo": (0.4, 0.4),
    "Kebun Binatang Surabaya": (0.4, 0.6),
    "Pakuwon City": (0.7, 0.7),
    "Marina": (0.3, 0.3),
}

edges = [
    ("Surabaya Pusat", "Tunjungan Plaza"),
    ("Surabaya Pusat", "Darmo"),
    ("Surabaya Pusat", "Kebun Binatang Surabaya"),
    ("Surabaya Timur", "Pakuwon City"),
    ("Surabaya Timur", "Surabaya Pusat"),
    ("Surabaya Barat", "Darmo"),
    ("Surabaya Barat", "Surabaya Pusat"),
    ("Surabaya Utara", "Tunjungan Plaza"),
    ("Surabaya Utara", "Surabaya Pusat"),
    ("Surabaya Selatan", "Darmo"),
    ("Surabaya Selatan", "Surabaya Pusat"),
    ("Tunjungan Plaza", "Surabaya Barat"),
    ("Pakuwon City", "Surabaya Utara"),
    ("Marina", "Surabaya Selatan"),
    ("Marina", "Darmo"),
]

def tabucol(graph, number_of_colors, tabu_size=10, reps=500, max_iterations=50000, debug=False):
    colors = list(range(number_of_colors))
    iterations = 0
    tabu = deque()
    solution = {node: colors[0] for node in graph.nodes}

    while iterations < max_iterations:
        move_candidates = set()
        conflict_count = 0
        for node1, node2 in graph.edges:
            if solution[node1] == solution[node2]:
                move_candidates.add(node1)
                move_candidates.add(node2)
                conflict_count += 1
        move_candidates = list(move_candidates)

        if conflict_count == 0:
            return solution

        for _ in range(reps):
            if not move_candidates:
                break
            node = choice(move_candidates)
            new_color = (solution[node] + 1) % number_of_colors

            new_solution = solution.copy()
            new_solution[node] = new_color
            new_conflicts = sum(
                1 for n1, n2 in graph.edges if new_solution[n1] == new_solution[n2]
            )
            if new_conflicts < conflict_count:
                solution = new_solution
                break

        iterations += 1
        if len(tabu) >= tabu_size:
            tabu.popleft()

    if debug:
        print(f"Failed after {iterations} iterations with {conflict_count} conflicts.")
    return None


def visualize_graph(graph, region_positions, coloring=None):
    """Visualize the graph with fixed positions and coloring."""
    plt.figure(figsize=(8, 6))
    
    pos = region_positions

    # Tentukan warna default jika coloring gagal
    if coloring:
        node_colors = [coloring[node] for node in graph.nodes]
    else:
        node_colors = "lightgray"

    nx.draw(
        graph, pos, with_labels=True,
        labels={node: node for node in graph.nodes},
        node_color=node_colors,
        cmap=plt.cm.rainbow, node_size=800, font_size=10, edge_color="gray"
    )
    plt.title("Peta Wilayah Surabaya dengan Pewarnaan", fontsize=16)
    plt.show()


if __name__ == "__main__":
    graph = nx.Graph()
    graph.add_edges_from(edges)

    # Coba dengan jumlah warna yang semakin besar jika gagal
    for num_colors in range(4, 10):
        print(f"Trying with {num_colors} colors...")
        coloring = tabucol(graph, num_colors, debug=True)
        if coloring:
            print(f"Success with {num_colors} colors!")
            break
    else:
        print("Failed to color the graph with up to 9 colors.")
        coloring = None

    # Visualize the graph
    visualize_graph(graph, regions, coloring=coloring)
