# test_final_state.py
import os
import subprocess
import stat

def test_build_router_executable():
    script_path = "/home/user/build_router.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_build_router_execution_and_output():
    script_path = "/home/user/build_router.sh"
    log_path = "/home/user/build_order.log"
    deps_path = "/home/user/deps.txt"

    # Ensure deps.txt exists
    assert os.path.isfile(deps_path), f"{deps_path} is missing."

    # Parse deps.txt to compute the expected build order
    deps_graph = {}
    with open(deps_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":", 1)
            target = parts[0].strip()
            deps = parts[1].strip().split() if len(parts) > 1 else []
            deps_graph[target] = deps

    visited = set()
    expected_order = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for dep in deps_graph.get(node, []):
            dfs(dep)
        expected_order.append(node)

    dfs("frontend")
    expected_log_lines = [f"[BUILD] {target}" for target in expected_order]

    # Clean up log file if it exists
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the script
    result = subprocess.run([script_path, "/build/frontend?dryrun=1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero status code: {result.returncode}\nStderr: {result.stderr}"

    # Check the log file
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        actual_log_lines = [line.strip() for line in f if line.strip()]

    assert actual_log_lines == expected_log_lines, (
        f"Build order in {log_path} is incorrect.\n"
        f"Expected: {expected_log_lines}\n"
        f"Actual: {actual_log_lines}"
    )