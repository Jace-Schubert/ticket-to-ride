import heapq
from utils import create_graph, get_neighbors

# Dijkstra's Algorithm (K-Shortest Paths)

def dijkstra(graph, source, destination, k=3):
    """
    Wrapper that returns k-shortest paths for use by the main module.
    """
    return k_shortest_paths(graph, source, destination, k)


def k_shortest_paths(graph, source, destination, k):
    
    num_cities = len(graph)
    # Min-heap: (cost, current_city, path_so_far)
    heap = [(0, source, [source])]
    results = []
    dest_count = 0

    while heap and dest_count < k:
        cost, current, path = heapq.heappop(heap)

        if current == destination:
            results.append((cost, path))
            dest_count += 1
            continue

        for neighbor, weight in get_neighbors(graph, current):
            if neighbor not in path:  # avoid loops within a single path
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))

    return results