# test_final_state.py

import os
import re
import pytest

def test_safe_append_source_fixed():
    source_path = "/home/user/tools/safe_append.c"
    assert os.path.isfile(source_path), f"Source file missing: {source_path}"

    with open(source_path, "r") as f:
        content = f.read()

    assert "flock" in content, "The flock() function call is missing in safe_append.c"
    assert "LOCK_EX" in content, "LOCK_EX is missing in safe_append.c"
    assert "LOCK_UN" in content, "LOCK_UN is missing in safe_append.c"

def test_safe_append_compiled():
    exe_path = "/home/user/tools/safe_append"
    assert os.path.isfile(exe_path), f"Compiled executable missing: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def test_api_docs_output():
    conf_path = "/home/user/docs.conf"
    assert os.path.isfile(conf_path), f"Config file missing: {conf_path}"

    prefix = ""
    with open(conf_path, "r") as f:
        for line in f:
            if line.startswith("PREFIX="):
                prefix = line.strip().split("=", 1)[1]
                break

    assert prefix, "Could not find PREFIX in docs.conf"

    src_dir = "/home/user/src"
    assert os.path.isdir(src_dir), f"Source directory missing: {src_dir}"

    src_files = sorted([f for f in os.listdir(src_dir) if f.endswith(".c")])

    expected_lines = []
    for src_file in src_files:
        with open(os.path.join(src_dir, src_file), "r") as f:
            in_api_block = False
            for line in f:
                stripped = line.strip()
                if stripped == "/* API":
                    in_api_block = True
                elif stripped == "*/":
                    in_api_block = False
                elif in_api_block:
                    expected_lines.append(f"{prefix} {line.rstrip('\n')}")

    expected_content = "\n".join(expected_lines)
    if expected_content:
        expected_content += "\n"

    output_path = "/home/user/api_docs.md"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {output_path} does not match expected output."