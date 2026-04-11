import heapq
from utils import get_neighbors

# Dijkstra's algorithm for shortest path
def dijkstra_shortest_path(graph, source, destination):
    # Initialize the number of cities
    num_cities = len(graph)

    # Min-heap: (cost, current_city, path_so_far)
    heap = [(0, source, [source])]

    # Set to keep track of visited cities
    visited = set()

    # Loop until the heap is empty
    while heap:
        cost, current, path = heapq.heappop(heap)

        # If we have reached the destination, return the cost and path
        if current == destination:
            return (cost, path)

        # If the current city has already been visited, skip it
        if current in visited:
            continue

        # Mark the current city as visited
        visited.add(current)

        # Explore neighbors of the current city
        for neighbor, weight in get_neighbors(graph, current):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))

    # If we don't reach the destination, return infinity and an empty path
    return (float('inf'), [])

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