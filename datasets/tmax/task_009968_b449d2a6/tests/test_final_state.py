# test_final_state.py
import os
import re

def test_responses_file_exists_and_correct():
    responses_file = "/home/user/responses.txt"
    assert os.path.exists(responses_file), f"File {responses_file} does not exist"

    with open(responses_file, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 50, f"Expected exactly 50 lines in {responses_file}, but found {len(lines)}"

    for i, line in enumerate(lines):
        val = line.strip()
        assert val == "5", f"Expected line {i+1} to be '5', but got '{val}'"

def test_benchmark_result_file_exists():
    benchmark_result_file = "/home/user/benchmark_result.txt"
    assert os.path.exists(benchmark_result_file), f"File {benchmark_result_file} does not exist"

    with open(benchmark_result_file, "r") as f:
        content = f.read().strip()

    assert len(content) > 0, f"File {benchmark_result_file} is empty"

def test_rpn_server_script_exists_and_valid():
    server_script = "/home/user/rpn_server.sh"
    assert os.path.exists(server_script), f"File {server_script} does not exist"
    assert os.access(server_script, os.X_OK), f"File {server_script} is not executable"

    with open(server_script, "r") as f:
        content = f.read()

    # Ensure bash arithmetic or let is used
    assert "$((" in content or "let " in content or "expr " in content, "rpn_server.sh does not appear to use bash arithmetic for evaluation"

    # Ensure no forbidden external tools are used for math
    forbidden_tools = ["awk", "bc", "python", "perl", "node", "ruby"]
    for tool in forbidden_tools:
        # Check for word boundaries to avoid matching substrings
        assert not re.search(rf'\b{tool}\b', content), f"rpn_server.sh must not use external tool '{tool}' for math evaluation"

def test_benchmark_script_exists():
    benchmark_script = "/home/user/benchmark.sh"
    assert os.path.exists(benchmark_script), f"File {benchmark_script} does not exist"
    assert os.access(benchmark_script, os.X_OK), f"File {benchmark_script} is not executable"