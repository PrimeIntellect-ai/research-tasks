# test_final_state.py

import os
import json
import subprocess
import pytest

def calculate_expected_score(v1, v2):
    file1 = f"/home/user/protos/{v1}/api.proto"
    file2 = f"/home/user/protos/{v2}/api.proto"

    assert os.path.isfile(file1), f"Expected proto file {file1} is missing."
    assert os.path.isfile(file2), f"Expected proto file {file2} is missing."

    # Run diff -U0
    cmd = ["diff", "-U0", file1, file2]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # diff returns 1 if files differ, 0 if same, 2 if error
    assert result.returncode in (0, 1), f"diff command failed: {result.stderr}"

    added = 0
    deleted = 0

    for line in result.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            deleted += 1

    score = (deleted * deleted * 3) + added
    return score

def test_rust_project_exists():
    cargo_toml = "/home/user/build_tools/impact_analyzer/Cargo.toml"
    main_rs = "/home/user/build_tools/impact_analyzer/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project manifest missing at {cargo_toml}"
    assert os.path.isfile(main_rs), f"Rust project source missing at {main_rs}"

def test_harness_script_exists_and_executable():
    script_path = "/home/user/test_harness.sh"
    assert os.path.isfile(script_path), f"Test harness script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Test harness script {script_path} is not executable"

def test_report_log_contains_correct_scores():
    report_path = "/home/user/report.log"
    assert os.path.isfile(report_path), f"Report log missing at {report_path}. Did the test harness run successfully?"

    expected_score_1 = calculate_expected_score("1.0.0", "1.1.0")
    expected_score_2 = calculate_expected_score("1.1.0", "2.0.0")

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content, f"{report_path} is empty."

    # Try to parse the log. It should contain two JSON objects, potentially separated by newlines.
    # Because grpcurl outputs standard JSON, we can extract all JSON objects.
    json_objects = []
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(content):
        # Skip whitespace
        while idx < len(content) and content[idx].isspace():
            idx += 1
        if idx >= len(content):
            break
        try:
            obj, end_idx = decoder.raw_decode(content[idx:])
            json_objects.append(obj)
            idx += end_idx
        except json.JSONDecodeError:
            # If we can't parse, just advance and try to find the next '{'
            next_brace = content.find('{', idx + 1)
            if next_brace == -1:
                break
            idx = next_brace

    assert len(json_objects) >= 2, f"Could not find at least two JSON objects in {report_path}. Content: {content}"

    scores = [obj.get("score") for obj in json_objects if "score" in obj]
    assert len(scores) >= 2, f"Could not find 'score' keys in the parsed JSON from {report_path}."

    assert scores[0] == expected_score_1, f"First score in report.log is {scores[0]}, expected {expected_score_1}"
    assert scores[1] == expected_score_2, f"Second score in report.log is {scores[1]}, expected {expected_score_2}"