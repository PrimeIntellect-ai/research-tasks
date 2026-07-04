# test_final_state.py

import os
import stat

def test_processor_executable_exists():
    executable_path = "/home/user/processor"
    assert os.path.exists(executable_path), f"The executable {executable_path} is missing."
    assert os.path.isfile(executable_path), f"The path {executable_path} is not a file."

    # Check if executable
    st = os.stat(executable_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"The file {executable_path} is not executable."

def test_clean_metrics_output():
    output_path = "/home/user/clean_metrics.csv"
    assert os.path.exists(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        actual_output = f.read().strip()

    expected_output = """timestamp,cpu_usage,memory_mb
1700000000,45,1024
1700000001,45,1024
1700000002,55,1040
1700000003,55,1040
1700000004,55,1040
1700000005,60,2048
1700000006,-1,-1
1700000007,-1,-1
1700000008,-1,-1
1700000009,-1,-1
1700000010,-1,-1
1700000011,-1,-1
1700000012,70,1024
1700000013,70,1024
1700000014,70,1024
1700000015,70,1024
1700000016,15,512"""

    # Normalize line endings
    actual_lines = [line.strip() for line in actual_output.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_output.splitlines() if line.strip()]

    assert actual_lines == expected_lines, "The generated clean_metrics.csv does not match the expected resampled and deduplicated output."