from union_find import UnionFind
from dijkstra import dijkstra
from utils import create_graph, get_graph, get_neighbors, gen_tickets


def build_railway_network(graph, tickets, node_count):
    """
    Main orchestration function.

    For each ticket:
      1. Use Dijkstra to find the shortest path
      2. Use Union-Find to check if adding the path creates a cycle
      3. If no cycle -> add path to the network
      4. If cycle -> remove the problem edge from the graph and
         run Dijkstra again to find an alternate path
    """

    # Initialize Union-Find for all nodes
    uf = UnionFind(node_count)

    # Stores the edges added to the railway
    final_network = []

    # Tracks the total cost of the network
    total_cost = 0

    for source, destination in tickets:
        print(f"\nProcessing ticket: {source} -> {destination}")

        # Keep track of edges already in the network (for reuse)
        existing_edges = set((u, v) for u, v, _ in final_network)

        # Make a copy of the graph so we can remove edges for retries
        temp_graph = [row[:] for row in graph]

        # Track edges we have removed to restore them later
        removed_edges = []

        path_added = False

        while not path_added:
            # Run standard Dijkstra on the (possibly modified) graph
            path_cost, path = dijkstra(temp_graph, source, destination)

            # No path found
            if not path or path_cost == float('inf'):
                print(f"No valid cycle-free path found for {source} -> {destination}")
                break

            # Extract edges from the path
            edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]

            # Only check new edges (skip edges already in the network)
            new_edges = [e for e in edges if e not in existing_edges]

            # Use a temporary Union-Find to test for cycles
            temp_uf = UnionFind(node_count)
            temp_uf.parent = uf.parent[:]
            temp_uf.rank = uf.rank[:]

            cycle_edge = None
            for u, v in new_edges:
                if not temp_uf.union(u, v):
                    cycle_edge = (u, v)
                    print(f"Cycle detected at edge {u} -> {v}, trying next path...")
                    break

            if cycle_edge is None:
                # No cycle - add the path to the network
                added_cost = 0
                for u, v in new_edges:
                    uf.union(u, v)
                    edge_weight = graph[u][v]
                    final_network.append((u, v, edge_weight))
                    added_cost += edge_weight

                total_cost += added_cost
                print(f"Path accepted: {path} (cost: {path_cost}, new edges cost: {added_cost})")
                path_added = True
            else:
                # Cycle detected - remove the problem edge and retry Dijkstra
                u, v = cycle_edge
                removed_edges.append((u, v, temp_graph[u][v]))
                temp_graph[u][v] = 0

    return final_network, total_cost

#------------------------------------------------------------
def main():

    graph = create_graph(*get_graph())
    node_count = len(graph)
    tickets = gen_tickets(node_count, 5)

    network, cost = build_railway_network(graph, tickets, node_count)

    # Display results
    print("\n" + "="*50)
    print("Final Railway Network:")
    for u, v, _ in network:
        print(f"   Edge: {u} → {v}")

    print(f"Total Network Cost: {cost}")


if __name__ == "__main__":
    main()
