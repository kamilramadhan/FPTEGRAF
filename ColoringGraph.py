import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from random import randrange, randint
import string


def generate_connected_graph(num_nodes, k_neighbors, prob):
    """Generate a connected Watts-Strogatz graph for more connections."""
    graph = nx.connected_watts_strogatz_graph(num_nodes, k_neighbors, prob)
    return graph


def tabucol(graph, number_of_colors, tabu_size=7, reps=100, max_iterations=10000, debug=False):
    colors = list(range(number_of_colors))
    iterations = 0
    tabu = deque()
    solution = {i: colors[randrange(0, len(colors))] for i in range(len(graph))}

    aspiration_level = {}

    while iterations < max_iterations:
        move_candidates = set()
        conflict_count = 0
        for i in range(len(graph)):
            for j in range(i + 1, len(graph)):
                if graph[i][j] > 0 and solution[i] == solution[j]:
                    move_candidates.add(i)
                    move_candidates.add(j)
                    conflict_count += 1
        move_candidates = list(move_candidates)

        if conflict_count == 0:
            break

        new_solution = None
        for _ in range(reps):
            node = move_candidates[randrange(0, len(move_candidates))]
            new_color = colors[randrange(0, len(colors) - 1)]
            if solution[node] == new_color:
                new_color = colors[-1]

            new_solution = solution.copy()
            new_solution[node] = new_color
            new_conflicts = 0
            for i in range(len(graph)):
                for j in range(i + 1, len(graph)):
                    if graph[i][j] > 0 and new_solution[i] == new_solution[j]:
                        new_conflicts += 1
            if new_conflicts < conflict_count:
                if new_conflicts <= aspiration_level.setdefault(conflict_count, conflict_count - 1):
                    aspiration_level[conflict_count] = new_conflicts - 1

                    if (node, new_color) in tabu:
                        tabu.remove((node, new_color))
                        if debug:
                            print("Tabu permitted;", conflict_count, "->", new_conflicts)
                        break
                else:
                    if (node, new_color) in tabu:
                        continue
                if debug:
                    print(conflict_count, "->", new_conflicts)
                break

        tabu.append((node, solution[node]))
        if len(tabu) > tabu_size:
            tabu.popleft()

        solution = new_solution
        iterations += 1
        if debug and iterations % 500 == 0:
            print("Iteration:", iterations)

    if conflict_count != 0:
        print("No coloring found with {} colors.".format(number_of_colors))
        return None
    else:
        print("Found coloring:\n", solution)
        return solution


def visualize_graph_side_by_side(graph, coloring=None):
    """Visualize uncolored and colored graphs side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    pos = nx.spring_layout(graph)
    labels = {i: chr(65 + i) for i in graph.nodes}

    # Uncolored graph
    nx.draw(graph, pos, with_labels=True, labels=labels, node_color="lightgray", ax=axes[0])
    axes[0].set_title("Graf Sebelum Pewarnaan")

    # Colored graph
    if coloring:
        colors = [coloring[node] for node in graph.nodes]
        nx.draw(graph, pos, with_labels=True, labels=labels, node_color=colors, cmap=plt.cm.rainbow, ax=axes[1])
        axes[1].set_title("Graf Setelah Pewarnaan (Tanpa Node Bertetangga Memiliki Warna Sama)")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    num_nodes = randint(10, 15)  # Random number of nodes between 10 and 15
    k_neighbors = 4  # Each node is connected to k neighbors
    edge_prob = 0.5  # Rewiring probability
    graph = generate_connected_graph(num_nodes, k_neighbors, edge_prob)

    # Visualize the uncolored graph and solve
    adjacency_matrix = nx.to_numpy_array(graph).astype(int).tolist()
    num_colors = randint(3, 6)  # Random number of colors between 3 and 6
    coloring = tabucol(adjacency_matrix, num_colors, debug=False)

    # Show side-by-side visualization
    visualize_graph_side_by_side(graph, coloring=coloring)
