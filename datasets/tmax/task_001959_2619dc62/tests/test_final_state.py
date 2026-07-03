# test_final_state.py

import os
import json
import subprocess
import re
import pytest

def get_max_semver(versions):
    def parse_version(v):
        v = v.lstrip('v')
        parts = v.split('.')
        return tuple(int(p) if p.isdigit() else 0 for p in parts)

    return max(versions, key=parse_version)

def test_patch_exists():
    patch_path = "/home/user/cjson-fix.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} does not exist."
    assert os.path.getsize(patch_path) > 0, f"Patch file {patch_path} is empty."

def test_libcjson_built():
    so_path = "/app/cJSON-1.7.15/libcjson.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist. Did you fix the Makefile and build it?"

def test_semver_parser_executable():
    exe_path = "/home/user/parser_app/semver_parser"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_highest_version_output():
    json_path = "/home/user/parser_app/versions.json"
    output_path = "/home/user/highest_version.txt"

    assert os.path.isfile(json_path), f"Input JSON {json_path} missing."
    with open(json_path, 'r') as f:
        try:
            versions = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {json_path} as JSON.")

    expected_max = get_max_semver(versions)

    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."
    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_max, f"Expected highest version {expected_max}, but got {actual_output}"

def test_valgrind_memory_leak():
    exe_path = "/home/user/parser_app/semver_parser"
    json_path = "/home/user/parser_app/versions.json"
    log_path = "/tmp/valgrind.log"

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/cJSON-1.7.15" + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")

    cmd = [
        "valgrind",
        "--leak-check=full",
        "--show-leak-kinds=definite",
        f"--log-file={log_path}",
        exe_path,
        json_path
    ]

    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Running semver_parser under valgrind failed. Stderr: {result.stderr}"

    assert os.path.isfile(log_path), "Valgrind log file was not generated."

    with open(log_path, "r") as f:
        log_content = f.read()

    match = re.search(r"definitely lost:\s+([0-9,]+)\s+bytes", log_content)
    assert match is not None, "Could not find 'definitely lost' metric in valgrind output."

    lost_bytes_str = match.group(1).replace(",", "")
    lost_bytes = int(lost_bytes_str)

    assert lost_bytes <= 0, f"Memory leak detected: {lost_bytes} bytes definitely lost. Threshold is 0."