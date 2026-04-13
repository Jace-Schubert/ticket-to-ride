import random

def create_graph(num_cities, edges):
    # Initialize an adjacency matrix with zeros
    graph = [[0] * num_cities for _ in range(num_cities)]

    # Fill the adjacency matrix with the given edges
    for source, destination, weight in edges:
        graph[source][destination] = weight

    return graph


def get_graph():
    """
    Returns the default Ticket to Ride graph as (num_cities, edges).
    Each edge is (source, destination, weight).
    Graph from assignment slides (8 cities, 0-7).
    """
    num_cities = 8
    edges = [
        (0, 3, 8), (0, 4, 4),
        (1, 0, 2), (1, 6, 11),
        (2, 5, 11), (2, 6, 1),
        (3, 1, 6), (3, 7, 9),
        (4, 6, 5),
        (5, 6, 2), (5, 7, 2),
        (6, 2, 4), (6, 4, 5),
        (7, 3, 2),
    ]
    return num_cities, edges


def get_neighbors(graph, city):
    # Initialize a list to store neighbors and their weights
    neighbors = []

    # Iterate through the row corresponding to the city in the adjacency matrix
    for dest, weight in enumerate(graph[city]):
        if weight > 0:
            neighbors.append((dest, weight))

    return neighbors

def gen_tickets(num_nodes_in_graph, ticket_count) -> list[int, int]:
    """
    Generates a random set of tickets for the Ticket to Ride problem.

    Parameters:
    -----------
    num_nodes_in_graph      : int  → Total number of nodes in the graph
    ticket_count            : int  → Number of tickets to generate

    Returns:
    --------
    tickets : list of (source, destination) tuples
    """

    # Use a set to automatically ignore duplicates
    tickets = set()

    while len(tickets) < ticket_count:
        source = random.randint(0, num_nodes_in_graph - 1)
        destination = random.randint(0, num_nodes_in_graph - 1)

        # Ensure source and destination are not the same node
        if source == destination:
            continue
        
        tickets.add((source, destination))

    return list(tickets)