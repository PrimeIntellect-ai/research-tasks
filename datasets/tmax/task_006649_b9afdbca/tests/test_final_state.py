# test_final_state.py

import os
import json
import re
import pytest

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/check_versions.sh",
        "/home/user/parse_mem.sh",
        "/home/user/api.sh",
        "/home/user/ci_pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_ci_result_json_content():
    result_path = "/home/user/ci_result.json"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    # Compute expected version_status
    lib_versions_path = "/home/user/lib_versions.txt"
    version_status = "LINK_OK"
    if os.path.isfile(lib_versions_path):
        with open(lib_versions_path, "r") as f:
            for line in f:
                if line.startswith("libmath_custom.so"):
                    parts = line.strip().split(" - ")
                    if len(parts) == 2:
                        v = parts[1]
                        v_parts = [int(x) for x in v.split(".")]
                        req_parts = [2, 4, 1]
                        if v_parts < req_parts:
                            version_status = "LINK_ERROR"
                        break

    # Compute expected mem_status
    valgrind_path = "/home/user/valgrind_mock.log"
    total_leaks = 0
    if os.path.isfile(valgrind_path):
        with open(valgrind_path, "r") as f:
            for line in f:
                m = re.search(r"\[WARN\] LEAK:\s+(\d+)\s+bytes", line)
                if m:
                    total_leaks += int(m.group(1))

    mem_status = f"MEM_FAIL: {total_leaks}" if total_leaks > 4096 else f"MEM_OK: {total_leaks}"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    assert "version_status" in data, "JSON missing 'version_status' key."
    assert data["version_status"] == version_status, f"Expected version_status '{version_status}', got '{data['version_status']}'."

    assert "mem_status" in data, "JSON missing 'mem_status' key."
    expected_mem = mem_status.replace(" ", "")
    actual_mem = str(data["mem_status"]).replace(" ", "")
    assert actual_mem == expected_mem, f"Expected mem_status '{mem_status}', got '{data['mem_status']}'."