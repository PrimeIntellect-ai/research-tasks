# test_final_state.py

import os
import re
import pytest

def test_extract_metrics_cpp_exists():
    cpp_file = "/home/user/extract_metrics.cpp"
    assert os.path.exists(cpp_file), f"{cpp_file} does not exist."
    assert os.path.isfile(cpp_file), f"{cpp_file} is not a file."

def test_extract_metrics_binary_exists_and_executable():
    bin_file = "/home/user/extract_metrics"
    assert os.path.exists(bin_file), f"{bin_file} does not exist."
    assert os.path.isfile(bin_file), f"{bin_file} is not a file."
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

def test_run_observability_script_exists_and_executable():
    sh_file = "/home/user/run_observability.sh"
    assert os.path.exists(sh_file), f"{sh_file} does not exist."
    assert os.path.isfile(sh_file), f"{sh_file} is not a file."
    assert os.access(sh_file, os.X_OK), f"{sh_file} is not executable."

def test_node_metrics_prom_format():
    prom_file = "/home/user/node_metrics.prom"
    assert os.path.exists(prom_file), f"{prom_file} does not exist. Did you run your shell script?"

    with open(prom_file, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, f"Output in {prom_file} must contain exactly two lines, found {len(content)}."

    match_utime = re.match(r'^worker_cpu_utime\{pid="(\d+)"\} (\d+)$', content[0])
    match_stime = re.match(r'^worker_cpu_stime\{pid="(\d+)"\} (\d+)$', content[1])

    assert match_utime is not None, f"First line format is incorrect. Got: {content[0]}"
    assert match_stime is not None, f"Second line format is incorrect. Got: {content[1]}"

    pid_utime = match_utime.group(1)
    pid_stime = match_stime.group(1)

    assert pid_utime == pid_stime, f"PIDs must match in both lines. Found {pid_utime} and {pid_stime}."