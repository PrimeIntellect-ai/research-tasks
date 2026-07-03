# test_final_state.py
import os
import pytest
import subprocess

def test_trace_script_exists_and_uses_cte():
    trace_path = "/home/user/trace.py"
    assert os.path.isfile(trace_path), f"Python script {trace_path} is missing."

    with open(trace_path, "r") as f:
        content = f.read().lower()

    assert "with recursive" in content or "with " in content, "The script /home/user/trace.py does not appear to use a Recursive CTE as requested."

def test_summarize_script_exists():
    summarize_path = "/home/user/summarize.sh"
    assert os.path.isfile(summarize_path), f"Bash script {summarize_path} is missing."

def test_raw_data_summary_output():
    summary_path = "/home/user/raw_data_summary.txt"
    assert os.path.isfile(summary_path), f"Output file {summary_path} was not created."

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Raw Data D content.",
        "Raw Data E content.",
        "Raw Data F content."
    ]

    unique_lines = sorted(list(set(lines)))
    assert unique_lines == expected_lines, f"Expected unique lines {expected_lines}, but got {unique_lines} in {summary_path}."

def test_trace_script_functionality():
    trace_path = "/home/user/trace.py"
    try:
        result = subprocess.run(
            ["python3", trace_path, "Final_Analysis_V3"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {trace_path} failed with error: {e.stderr}")

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    expected_paths = [
        "/home/user/data/raw_d.txt",
        "/home/user/data/raw_e.txt",
        "/home/user/data/raw_f.txt"
    ]

    unique_output_paths = sorted(list(set(output_lines)))
    assert unique_output_paths == expected_paths, f"Expected paths {expected_paths}, but got {unique_output_paths} from trace.py output."