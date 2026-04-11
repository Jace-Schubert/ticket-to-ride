import random

def create_graph(num_cities, edges):
    # Initialize an adjacency matrix with zeros
    graph = [[0] * num_cities for _ in range(num_cities)]

    # Fill the adjacency matrix with the given edges
    for source, destination, weight in edges:
        graph[source][destination] = weight

    return graph


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