# test_final_state.py

import os
import stat
import subprocess
import glob
import pytest

def test_router_conf_updated():
    path = "/home/user/router.conf"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "/tmp/metrics_backend.sock" in content, "router.conf does not point to the correct socket path: /tmp/metrics_backend.sock"

def test_report_content_and_permissions():
    path = "/home/user/502_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check permissions
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions of {path} are {oct(perms)}, expected 0o400 strictly read-only for owner."

    # Check content
    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, found {len(lines)}."
    for line in lines:
        assert "502 Bad Gateway" in line, f"Line in report does not contain '502 Bad Gateway': {line}"

def test_timezone_configured():
    # The timezone can be set in the C++ code or via the environment variable TZ
    path = "/home/user/backend/server.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    if "Asia/Tokyo" in content:
        return # Timezone configured in code

    # Check running 'server' process environments
    found_tz = False
    for comm_file in glob.glob("/proc/[0-9]*/comm"):
        try:
            with open(comm_file, "r") as f:
                comm = f.read().strip()
            if comm == "server":
                pid = comm_file.split("/")[2]
                with open(f"/proc/{pid}/environ", "rb") as f:
                    env = f.read()
                if b"TZ=Asia/Tokyo" in env:
                    found_tz = True
                    break
        except Exception:
            continue

    assert found_tz, "Timezone 'Asia/Tokyo' not found in server.cpp or running 'server' process environment (TZ variable)."

def test_benchmark_performance():
    script_path = "/home/user/benchmark.sh"
    assert os.path.isfile(script_path), f"Benchmark script {script_path} not found."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Benchmark script failed with error: {result.stderr}"

    try:
        execution_time = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Benchmark script did not output a valid float: {result.stdout}")

    threshold = 1.5
    assert execution_time <= threshold, f"Execution time {execution_time}s exceeds threshold of {threshold}s. The C++ backend is not optimized enough."