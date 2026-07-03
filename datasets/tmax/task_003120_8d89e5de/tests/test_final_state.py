# test_final_state.py

import os
import re
import pytest

def test_throughput_metric():
    results_file = '/home/user/results.txt'
    assert os.path.isfile(results_file), f"File {results_file} does not exist."

    with open(results_file, 'r') as f:
        content = f.read()

    match = re.search(r'Throughput:\s*([\d\.]+)\s*pps', content)
    assert match is not None, f"Could not find 'Throughput: <number> pps' in {results_file}. Content was: {content}"

    pps = float(match.group(1))
    assert pps >= 5000.0, f"Throughput {pps} pps is less than the required threshold of 5000.0 pps."

def test_monitor_script_exists_and_executable():
    script_file = '/home/user/monitor.sh'
    assert os.path.isfile(script_file), f"File {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"File {script_file} is not executable."

def test_monitor_script_logic():
    script_file = '/home/user/monitor.sh'
    assert os.path.isfile(script_file), f"File {script_file} does not exist."

    with open(script_file, 'r') as f:
        content = f.read()

    # Check that the script contains references to the required log files and the 1000 byte threshold
    assert 'probe.log' in content, f"{script_file} does not reference 'probe.log'."
    assert '1000' in content, f"{script_file} does not reference the 1000 byte limit."
    assert 'probe.log.1' in content, f"{script_file} does not reference 'probe.log.1'."
    assert 'probe.log.2' in content, f"{script_file} does not reference 'probe.log.2'."