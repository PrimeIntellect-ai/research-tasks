# test_final_state.py

import os
import subprocess
import re
import ast

def test_etl_script_exists():
    assert os.path.isfile("/home/user/etl.py"), "The script /home/user/etl.py does not exist."

def test_etl_uses_multiprocessing():
    with open("/home/user/etl.py", "r", encoding="utf-8") as f:
        code = f.read()

    # Check for multiprocessing or concurrent.futures imports
    tree = ast.parse(code)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    has_parallel_lib = any(
        imp.startswith("multiprocessing") or imp.startswith("concurrent.futures")
        for imp in imports
    )
    assert has_parallel_lib, "The script must use 'multiprocessing' or 'concurrent.futures' for parallel processing."

def test_etl_execution_and_idempotency():
    # Run the script to ensure it executes correctly and is idempotent
    result = subprocess.run(
        ["python3", "/home/user/etl.py", "/home/user/input", "/home/user/output"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"etl.py failed to execute. Stderr: {result.stderr}"

def test_output_summary_content():
    summary_path = "/home/user/output/summary.txt"
    assert os.path.isfile(summary_path), f"The output file {summary_path} does not exist."

    with open(summary_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "Hour: 2023-10-01T10:00:00Z | Unique Langs: 2 | Sample: Hello",
        "Hour: 2023-10-01T11:00:00Z | Unique Langs: 2 | Sample: Bonjour",
        "Hour: 2023-10-02T08:00:00Z | Unique Langs: 1 | Sample: مرحبا"
    ]

    actual_lines = content.split("\n")
    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in summary.txt, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual.strip()}'"

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Total unique records: 5" in content, "The log file does not contain the expected 'Total unique records: 5' message."