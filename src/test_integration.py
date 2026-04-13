from main import build_railway_network
from utils import create_graph, get_graph


def run_test(test_name, tickets, expected_edges, expected_cost):
    """
    Runs a single integration test case.

    Parameters:
    -----------
    test_name       : str   -> Description of the test
    tickets         : list  -> List of (source, destination) tuples
    expected_edges  : list  -> Expected edges in final network [(u, v), ...]
    expected_cost   : int   -> Expected total network cost
    """

    graph = create_graph(*get_graph())
    node_count = len(graph)

    print("=" * 60)
    print(f"TEST: {test_name}")
    print(f"Input tickets: {tickets}")
    print("-" * 60)

    network, cost = build_railway_network(graph, tickets, node_count)
    actual_edges = [(u, v) for u, v, _ in network]

    print(f"\nActual edges:   {actual_edges}")
    print(f"Actual cost:    {cost}")

    edges_pass = actual_edges == expected_edges
    cost_pass = cost == expected_cost

    if edges_pass and cost_pass:
        print(">> PASSED")
    else:
        if not edges_pass:
            print(f">> FAILED (edges mismatch)")
            print(f"   Expected: {expected_edges}")
        if not cost_pass:
            print(f">> FAILED (cost mismatch)")
            print(f"   Expected: {expected_cost}")

    print("=" * 60 + "\n")
    return edges_pass and cost_pass


def main():
    results = []

    # ----------------------------------------------------------
    # Test 1: Basic single ticket - shortest path
    # Shortest path from 0 to 7: 0->3 (8) + 3->7 (9) = 17
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="1 - Basic single ticket (shortest path)",
        tickets=[(0, 7)],
        expected_edges=[(0, 3), (3, 7)],
        expected_cost=17
    ))

    # ----------------------------------------------------------
    # Test 2: Two tickets with edge reuse
    # Ticket 1: 0->7 via 0->3->7 (cost 17, new cost 17)
    # Ticket 2: 0->6 via 0->4->6 (cost 9, new cost 9)
    #           No overlapping edges, both connect to node 0
    # Total: 17 + 9 = 26
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="2 - Two tickets from same source",
        tickets=[(0, 7), (0, 6)],
        expected_edges=[(0, 3), (3, 7), (0, 4), (4, 6)],
        expected_cost=26
    ))

    # ----------------------------------------------------------
    # Test 3: Unreachable destination (node 6 has no outgoing edges)
    # Should return empty network with cost 0
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="3 - Unreachable destination (dead-end source node)",
        tickets=[(6, 0)],
        expected_edges=[],
        expected_cost=0
    ))

    # ----------------------------------------------------------
    # Test 4: Cycle detection - shortest paths rejected
    # Ticket 1: 0->7 via 0->3->7 (connects {0,3,7})
    # Ticket 2: 1->7 via 1->5->7 (connects {1,5} to {0,3,7} = {0,1,3,5,7})
    # Ticket 3: 1->6, shortest is 1->0->4->6 (cost 11) but
    #           edge 1->0 creates a cycle (1 and 0 already connected)
    #           Falls back to 1->5->6 (cost 13), reuses 1->5,
    #           only adds 5->6 (new cost 2)
    # Ticket 4: 0->6, shortest is 0->4->6 (cost 9) but
    #           edge 4->6 creates a cycle (0 and 6 already connected)
    #           No other valid path found
    # Total: 17 + 14 + 2 + 0 = 33
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="4 - Cycle detection rejects shortest paths",
        tickets=[(0, 7), (1, 7), (1, 6), (0, 6)],
        expected_edges=[(0, 3), (3, 7), (1, 5), (5, 7), (5, 6)],
        expected_cost=33
    ))

    # ----------------------------------------------------------
    # Test 5: Multiple independent tickets building a tree
    # Ticket 1: 0->6 via 0->4->6 (cost 9)
    # Ticket 2: 2->6 via 2->6 (cost 4)
    # Ticket 3: 1->7 via 1->5->7 (cost 14)
    # All paths are independent, no overlap, no cycles
    # Total: 9 + 4 + 14 = 27
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="5 - Multiple independent tickets (no overlap)",
        tickets=[(0, 6), (2, 6), (1, 7)],
        expected_edges=[(0, 4), (4, 6), (2, 6), (1, 5), (5, 7)],
        expected_cost=27
    ))

    # ----------------------------------------------------------
    # Test 6: Mixed - valid paths, unreachable, and edge reuse
    # Ticket 1: 0->7 via 0->3->7 (cost 17)
    # Ticket 2: 7->1 no path (node 7 is a dead end)
    # Ticket 3: 0->6 via 0->4->6 (cost 9, new cost 9)
    # Total: 17 + 9 = 26
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="6 - Mixed: valid, unreachable, and edge reuse",
        tickets=[(0, 7), (7, 1), (0, 6)],
        expected_edges=[(0, 3), (3, 7), (0, 4), (4, 6)],
        expected_cost=26
    ))

    # ----------------------------------------------------------
    # Summary
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    for i, result in enumerate(results, 1):
        status = "PASSED" if result else "FAILED"
        print(f"  Test {i}: {status}")
    print(f"\n  {passed}/{total} tests passed")
    print("=" * 60)


if __name__ == "__main__":
    main()
