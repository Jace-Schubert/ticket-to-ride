import heapq
from utils import get_neighbors

def dijkstra(graph, source, destination, k=3):
    """
    Wrapper that returns k-shortest paths for use by the main module.
    """
    return k_shortest_paths(graph, source, destination, k)

# K-Shortest Paths
def k_shortest_paths(graph, source, destination, k):
    # Initialize the number of cities
    num_cities = len(graph)

    # Min-heap: (cost, current_city, path_so_far)
    heap = [(0, source, [source])]

    # List to store the k shortest paths found
    results = []

    # Counter for the number of paths found to the destination
    dest_count = 0

    # Loop until the heap is empty and we have found k paths to the destination
    while heap and dest_count < k:
        # Pop the path with the lowest cost
        cost, current, path = heapq.heappop(heap)

        # If we have reached the destination, add the cost and path to results
        if current == destination:
            results.append((cost, path))
            dest_count += 1
            continue

        # Explore neighbors of the current city
        for neighbor, weight in get_neighbors(graph, current):
            if neighbor not in path:  # avoid loops within a single path
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))

    return results