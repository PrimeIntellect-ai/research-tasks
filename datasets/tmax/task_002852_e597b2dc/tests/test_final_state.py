# test_final_state.py
import os

def test_results_txt_contents():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "15,3.1,32.0",
        "13,2.1,25.0",
        "12,2.0,15.0",
        "14,3.0,10.0"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {results_path} do not match expected output. Got:\n{actual_lines}\nExpected:\n{expected_lines}"

def test_query_tool_cpp_binding():
    cpp_path = "/home/user/query_tool.cpp"
    assert os.path.exists(cpp_path), f"{cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "sqlite3_bind_" in content, "No parameter binding (sqlite3_bind_*) detected in source code. You must use parameterized queries."