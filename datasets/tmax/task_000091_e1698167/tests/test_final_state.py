# test_final_state.py
import os
import sys
import json
from decimal import Decimal

def test_final_report_content():
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Final report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "SUCCESS: VALIDATION_PASSED_FLAG_88219"
    assert content == expected_content, f"Expected final report to contain '{expected_content}', but found '{content}'."

def test_calculator_precision():
    sys.path.insert(0, "/home/user/legacy_sim")
    try:
        from calculator import compute_precise_sum
    except ImportError:
        assert False, "Could not import compute_precise_sum from calculator.py"
    finally:
        sys.path.pop(0)

    result = compute_precise_sum(10)
    assert isinstance(result, Decimal), f"compute_precise_sum should return a Decimal object, but returned {type(result).__name__}."
    assert str(result) == "1.0", f"compute_precise_sum(10) should equal 1.0, but got {result}."

def test_tree_resolver_recursion():
    sys.path.insert(0, "/home/user/legacy_sim")
    try:
        from tree_resolver import count_nodes
    except ImportError:
        assert False, "Could not import count_nodes from tree_resolver.py"
    finally:
        sys.path.pop(0)

    graph_path = "/home/user/legacy_sim/data/graph.json"
    assert os.path.isfile(graph_path), f"Graph data file {graph_path} is missing."

    with open(graph_path, "r") as f:
        graph = json.load(f)

    try:
        count = count_nodes("A", graph)
    except RecursionError:
        assert False, "count_nodes raised a RecursionError. Cyclic dependencies are not handled properly."

    assert count == 4, f"count_nodes('A', graph) should return 4 unique nodes, but returned {count}."