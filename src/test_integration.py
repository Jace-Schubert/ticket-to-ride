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
    # Test 2: Two tickets with edge reuse and cycle detection
    # Ticket 1: 0->7 via 0->3->7 (cost 17, connects {0,3,7})
    # Ticket 2: 3->6, shortest is 3->1->0->4->6 (cost 17) but
    #           1->0 creates cycle (0 and 3 already connected)
    #           Falls back to 3->1->6 (cost 17), adds 3->1, 1->6
    # Total: 17 + 17 = 34
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="2 - Edge reuse with cycle detection",
        tickets=[(0, 7), (3, 6)],
        expected_edges=[(0, 3), (3, 7), (3, 1), (1, 6)],
        expected_cost=34
    ))

    # ----------------------------------------------------------
    # Test 3: All paths create cycles (no valid path for 2nd ticket)
    # Ticket 1: 0->7 via 0->3->7 (cost 17, connects {0,3,7})
    # Ticket 2: 7->0, every path from 7 goes through 7->3
    #           but 7 and 3 are already connected, creating a cycle
    #           No valid cycle-free path exists
    # Total: 17
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="3 - No valid cycle-free path exists",
        tickets=[(0, 7), (7, 0)],
        expected_edges=[(0, 3), (3, 7)],
        expected_cost=17
    ))

    # ----------------------------------------------------------
    # Test 4: Cycle detection - shortest path rejected, reuses edges
    # Ticket 1: 0->7 via 0->3->7 (cost 17, connects {0,3,7})
    # Ticket 2: 3->6, shortest is 3->1->0->4->6 (cost 17) but
    #           1->0 creates cycle (0 and 3 already connected)
    #           Falls back to 3->1->6 (cost 17), connects {0,1,3,6,7}
    # Ticket 3: 0->6, shortest is 0->4->6 (cost 9) but
    #           4->6 creates cycle (0 and 6 already connected)
    #           Falls back to 0->3->1->6 (cost 25) which reuses
    #           all existing edges (new cost 0)
    # Total: 17 + 17 + 0 = 34
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="4 - Cycle detection rejects shortest, falls back to reuse",
        tickets=[(0, 7), (3, 6), (0, 6)],
        expected_edges=[(0, 3), (3, 7), (3, 1), (1, 6)],
        expected_cost=34
    ))

    # ----------------------------------------------------------
    # Test 5: Multiple independent tickets building a tree
    # Ticket 1: 0->6 via 0->4->6 (cost 4+5 = 9)
    # Ticket 2: 2->7 via 2->5->7 (cost 11+2 = 13)
    # Ticket 3: 3->0 via 3->1->0 (cost 6+2 = 8)
    # All paths are independent, no overlap, no cycles
    # Total: 9 + 13 + 8 = 30
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="5 - Multiple independent tickets (no overlap)",
        tickets=[(0, 6), (2, 7), (3, 0)],
        expected_edges=[(0, 4), (4, 6), (2, 5), (5, 7), (3, 1), (1, 0)],
        expected_cost=30
    ))

    # ----------------------------------------------------------
    # Test 6: Three tickets, all valid, no cycles
    # Ticket 1: 0->7 via 0->3->7 (cost 8+9 = 17)
    # Ticket 2: 2->7 via 2->5->7 (cost 11+2 = 13)
    # Ticket 3: 0->6 via 0->4->6 (cost 4+5 = 9)
    # All independent paths, no shared edges, no cycles
    # Total: 17 + 13 + 9 = 39
    # ----------------------------------------------------------
    results.append(run_test(
        test_name="6 - Three valid tickets with no conflicts",
        tickets=[(0, 7), (2, 7), (0, 6)],
        expected_edges=[(0, 3), (3, 7), (2, 5), (5, 7), (0, 4), (4, 6)],
        expected_cost=39
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
