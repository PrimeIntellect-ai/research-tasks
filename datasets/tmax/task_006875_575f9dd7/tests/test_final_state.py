# test_final_state.py
import os
import glob

def test_parse_build_script_exists():
    script_path = "/home/user/parse_build.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_missing_lib_extracted_correctly():
    missing_lib_path = "/home/user/missing_lib.txt"
    assert os.path.isfile(missing_lib_path), f"The file {missing_lib_path} does not exist."

    with open(missing_lib_path, "r") as f:
        content = f.read().strip()

    assert content == "TelemetryEngineX", f"Expected missing_lib.txt to contain 'TelemetryEngineX', but got '{content}'"

def test_merged_build_log():
    merged_log_path = "/home/user/merged_build.log"
    assert os.path.isfile(merged_log_path), f"The file {merged_log_path} does not exist."

    # Read all original logs to get the expected lines
    original_lines = []
    log_files = glob.glob("/home/user/build_logs/worker_*.log")
    for log_file in log_files:
        with open(log_file, "r") as f:
            original_lines.extend(f.read().splitlines())

    # Read the merged log
    with open(merged_log_path, "r") as f:
        merged_lines = f.read().splitlines()

    # Check that the number of lines matches
    assert len(merged_lines) == len(original_lines), f"Expected {len(original_lines)} lines in merged log, but got {len(merged_lines)}."

    # Check that the merged log contains all original lines
    assert sorted(merged_lines) == sorted(original_lines), "The merged log does not contain the exact same lines as the original logs."

    # Check that the merged log is sorted by timestamp
    # The timestamp is at the beginning of each line, so lexicographical sorting of lines 
    # should match the chronological sorting since the format is [YYYY-MM-DDTHH:MM:SS.mmmZ]
    expected_sorted_lines = sorted(original_lines)
    assert merged_lines == expected_sorted_lines, "The merged log is not chronologically sorted."