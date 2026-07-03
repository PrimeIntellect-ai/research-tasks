# test_final_state.py
import os
import sys

def test_build_order_txt():
    """Verify the generated build_order.txt contains the correct topological sort."""
    build_order_file = "/home/user/polybuild/build_order.txt"
    assert os.path.isfile(build_order_file), f"{build_order_file} does not exist."

    with open(build_order_file, "r") as f:
        content = f.read().strip()

    expected = "logger, database, api, frontend"
    assert content == expected, f"Expected build order '{expected}', but got '{content}'."

def test_test_results_log():
    """Verify that test_results.log was generated and contains pytest output."""
    log_file = "/home/user/polybuild/test_results.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    assert "passed" in content.lower() or "test session starts" in content, "test_results.log does not look like valid pytest output."

def test_test_parser_exists():
    """Verify that the test suite was created."""
    test_file = "/home/user/polybuild/test_parser.py"
    assert os.path.isfile(test_file), f"{test_file} does not exist."

def test_build_parser_logic():
    """Verify the logic in build_parser.py has been fixed."""
    sys.path.insert(0, "/home/user/polybuild")
    try:
        import build_parser
    except ImportError:
        assert False, "Could not import build_parser.py"

    # Test version logic
    assert hasattr(build_parser, "check_version"), "check_version function is missing."
    # 1.10.0 >= 1.2.0 should be True now
    assert build_parser.check_version("1.10.0", "1.2.0") is True, "check_version failed: 1.10.0 should be >= 1.2.0"
    assert build_parser.check_version("1.2.0", "1.10.0") is False, "check_version failed: 1.2.0 should not be >= 1.10.0"
    assert build_parser.check_version("2.0.0", "2.0.0") is True, "check_version failed: 2.0.0 should be >= 2.0.0"

    # Test graph traversal logic
    assert hasattr(build_parser, "get_build_order"), "get_build_order function is missing."

    mock_targets = {
        'A': {'version': '1.0.0', 'depends': ['B@>=1.0.0']},
        'B': {'version': '1.0.0', 'depends': ['C@>=1.0.0']},
        'C': {'version': '1.0.0', 'depends': []}
    }

    try:
        order = build_parser.get_build_order(mock_targets)
    except Exception as e:
        assert False, f"get_build_order raised an exception: {e}"

    assert order == ['C', 'B', 'A'], f"get_build_order returned {order}, expected ['C', 'B', 'A']"