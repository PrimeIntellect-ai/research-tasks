# test_final_state.py

import os
import re
import pytest

PIPELINE_DIR = "/home/user/pipeline"
PROCESS_SH = os.path.join(PIPELINE_DIR, "process.sh")
MAKEFILE = os.path.join(PIPELINE_DIR, "Makefile")
C_FILE = os.path.join(PIPELINE_DIR, "manifest_parser.c")
OUTPUT_JSON = os.path.join(PIPELINE_DIR, "output.json")
EXECUTABLE = os.path.join(PIPELINE_DIR, "manifest_parser")

def test_process_sh_exists_and_executable():
    assert os.path.isfile(PROCESS_SH), f"{PROCESS_SH} does not exist."
    assert os.access(PROCESS_SH, os.X_OK), f"{PROCESS_SH} is not executable."

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE), f"{MAKEFILE} does not exist."
    with open(MAKEFILE, "r") as f:
        content = f.read()

    assert "-Wall" in content, "Makefile does not contain the '-Wall' flag."
    assert "-o manifest_parser" in content or "manifest_parser:" in content, "Makefile does not specify the output executable name 'manifest_parser'."

def test_c_code_fixed():
    assert os.path.isfile(C_FILE), f"{C_FILE} does not exist."
    with open(C_FILE, "r") as f:
        content = f.read()

    # Check for buffer size 128
    assert re.search(r"char\s+value\s*\[\s*128\s*\]\s*;", content), "manifest_parser.c does not declare 'char value[128];'."

    # Check for constrained format string like %127s or %127[^\n]
    assert re.search(r"%127s|%127\[", content), "manifest_parser.c does not constrain the fscanf reading mechanism (e.g., %127s)."

def test_output_json_correct():
    assert os.path.isfile(OUTPUT_JSON), f"{OUTPUT_JSON} does not exist."
    with open(OUTPUT_JSON, "r") as f:
        content = f.read().strip()

    expected_lines = [
        '{"APP_NAME": "SuperMobileApp"}',
        '{"BUILD_ID": "99281"}',
        '{"MALICIOUS_INJECT": "' + 'A' * 127 + '"}'
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, "output.json does not match the expected JSON output."

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"The executable {EXECUTABLE} was not built."
    assert os.access(EXECUTABLE, os.X_OK), f"The file {EXECUTABLE} is not executable."