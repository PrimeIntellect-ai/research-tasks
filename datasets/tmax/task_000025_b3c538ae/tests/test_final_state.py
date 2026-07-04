# test_final_state.py
import os
import sys
import pytest

def test_protobuf_compiled():
    path = "/home/user/build_graph_pb2.py"
    assert os.path.isfile(path), f"Compiled Protobuf file missing: {path}"

def test_test_solver_file_created():
    path = "/home/user/test_solver.py"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "test_solver.py does not import/use hypothesis"
    assert "@given" in content or "@settings" in content, "test_solver.py does not use hypothesis decorators (@given or @settings)"

def test_test_report_generated():
    path = "/home/user/test_report.txt"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read().lower()

    assert "test session starts" in content or "passed" in content, "test_report.txt does not look like a valid pytest output"

def test_solver_logic():
    sys.path.insert(0, '/home/user')
    try:
        import build_graph_pb2
        from solver import resolve_build_order
    except ImportError as e:
        pytest.fail(f"Failed to import compiled protobuf or solver.py: {e}")

    # Test valid graph with alphabetical tie-breaking
    g = build_graph_pb2.BuildGraph()
    m1 = g.modules.add()
    m1.name = "A"
    m1.depends_on.extend(["B", "C"])

    m2 = g.modules.add()
    m2.name = "B"
    m2.depends_on.extend(["D"])

    m3 = g.modules.add()
    m3.name = "C"
    m3.depends_on.extend(["D"])

    m4 = g.modules.add()
    m4.name = "D"

    order = resolve_build_order(g)
    expected = ["D", "B", "C", "A"]
    actual = list(order.ordered_modules)
    assert actual == expected, f"Expected build order {expected}, but got {actual}"

    # Test cycle detection
    g2 = build_graph_pb2.BuildGraph()
    c1 = g2.modules.add()
    c1.name = "X"
    c1.depends_on.extend(["Y"])
    c2 = g2.modules.add()
    c2.name = "Y"
    c2.depends_on.extend(["X"])

    with pytest.raises(ValueError) as excinfo:
        resolve_build_order(g2)

    assert "Cycle detected" in str(excinfo.value), "Expected ValueError with 'Cycle detected' message when a cycle is present"