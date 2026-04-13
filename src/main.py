from union_find import UnionFind
from dijkstra import dijkstra
from utils import create_graph, get_graph, get_neighbors, gen_tickets


def build_railway_network(graph, tickets, node_count):
    """
    Main orchestration function.
    
    For each ticket:
      1. Use Dijkstra to get candidate paths (shortest first)
      2. Use Union-Find to check if adding the path creates a cycle
      3. If no cycle -> add path to the network
      4. If cycle -> try next shortest path
    """

    # Initialize Union-Find for all nodes
    uf = UnionFind(node_count) 

    # Stores the edges added to the railway
    final_network = []

    # Tracks the total cost of the network         
    total_cost = 0              

    for source, destination in tickets:
        print(f"\nProcessing ticket: {source} -> {destination}")

        # Get all possible paths sorted by cost
        candidate_paths = dijkstra(graph, source, destination, node_count)

        if not candidate_paths:
            print(f"No path found for ticket {source} -> {destination}")
            continue

        # Try each path (shortest first) until one is cycle-free
        path_added = False
        existing_edges = set((u, v) for u, v, _ in final_network)

        for path_cost, path in candidate_paths:
            edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]

            # Only check new edges (skip edges already in the network)
            new_edges = [e for e in edges if e not in existing_edges]

            temp_uf = UnionFind(node_count)
            temp_uf.parent = uf.parent[:]
            temp_uf.rank = uf.rank[:]

            cycle_detected = False
            for u, v in new_edges:
                if not temp_uf.union(u, v):
                    cycle_detected = True
                    print(f"Cycle detected at edge {u} -> {v}, trying next path...")
                    break

            if not cycle_detected:
                added_cost = 0
                for u, v in new_edges:
                    uf.union(u, v)
                    edge_weight = graph[u][v]
                    final_network.append((u, v, edge_weight))
                    added_cost += edge_weight

                total_cost += added_cost
                print(f"Path accepted: {path} (cost: {path_cost}, new edges cost: {added_cost})")
                path_added = True
                break

        if not path_added:
            print(f"No valid cycle-free path found for {source} -> {destination}")

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