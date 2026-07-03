# test_final_state.py
import os

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_profile_summary_contents():
    summary_path = "/home/user/profile_summary.txt"
    assert os.path.isfile(summary_path), f"Output file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "25 web,frontend,us-east",
        "15 db,backend,us-west",
        "5 cache,backend,none",
        "5 cache,backend,us-east"
    ]

    assert lines == expected_lines, (
        f"Contents of {summary_path} do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(lines)}"
    )