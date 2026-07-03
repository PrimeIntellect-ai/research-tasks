# test_final_state.py

import os
import sys

def test_success_log():
    log_path = '/home/user/success.log'
    assert os.path.isfile(log_path), f"Expected success log at {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert content == "ALL TESTS PASSED", f"Expected success log to contain 'ALL TESTS PASSED', got '{content}'"

def test_dag_logic():
    sys.path.insert(0, '/home/user/project')
    try:
        from dag import resolve_dependencies
    except ImportError:
        assert False, "Could not import resolve_dependencies from /home/user/project/dag.py"

    # Test Linear
    graph_linear = {'A': ['B'], 'B': ['C'], 'C': []}
    assert resolve_dependencies(graph_linear) == ['C', 'B', 'A'], "Linear dependency resolution failed."

    # Test Diamond (This tests if the recursion stack state bug was fixed)
    graph_diamond = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    try:
        result = resolve_dependencies(graph_diamond)
    except ValueError as e:
        assert False, f"Diamond dependency resolution failed with ValueError: {e}. The DFS recursion stack state (visiting) might not be properly managed."

    assert result.index('D') < result.index('B'), "Diamond dependency resolution order incorrect (D must precede B)."
    assert result.index('D') < result.index('C'), "Diamond dependency resolution order incorrect (D must precede C)."
    assert result.index('B') < result.index('A'), "Diamond dependency resolution order incorrect (B must precede A)."
    assert result.index('C') < result.index('A'), "Diamond dependency resolution order incorrect (C must precede A)."

    # Test Cycle (This tests if the patch was applied correctly)
    graph_cycle = {'A': ['B'], 'B': ['C'], 'C': ['A']}
    cycle_detected = False
    try:
        resolve_dependencies(graph_cycle)
    except ValueError as e:
        if "Cycle detected" in str(e):
            cycle_detected = True

    assert cycle_detected, "Cycle dependency was not detected. The patch might not have been applied or the ValueError message is incorrect."