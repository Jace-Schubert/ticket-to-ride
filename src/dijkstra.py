import heapq
from utils import get_neighbors


def dijkstra(graph, source, destination):
    """
    Standard Dijkstra's algorithm to find the shortest path
    from source to destination in a weighted directed graph.

    Parameters:
    -----------
    graph       : 2D list  -> Adjacency matrix
    source      : int      -> Starting node
    destination : int      -> Target node

    Returns:
    --------
    (cost, path) : tuple -> Shortest path cost and list of nodes
                   Returns (float('inf'), []) if no path exists
    """

    # Min-heap: (cost, current_city, path_so_far)
    heap = [(0, source, [source])]

    # Track visited nodes to avoid revisiting
    visited = set()

    while heap:
        # Pop the node with the lowest cost
        cost, current, path = heapq.heappop(heap)

        # If we reached the destination, return the cost and path
        if current == destination:
            return (cost, path)

        # Skip nodes we have already visited
        if current in visited:
            continue
        visited.add(current)

        # Explore neighbors of the current node
        for neighbor, weight in get_neighbors(graph, current):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))

    # No path found
    return (float('inf'), [])
