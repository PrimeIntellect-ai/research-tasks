# test_final_state.py

import os
import re
import stat
import pytest

def test_test_sim_script_exists_and_executable():
    path = "/home/user/test_sim.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_fix_sim_script_exists_and_executable():
    path = "/home/user/fix_sim.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_sim_stats_output():
    path = "/home/user/sim_stats.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run test_sim.sh?"

    with open(path, "r") as f:
        content = f.read().strip()

    pattern = r"^Unique:\s*([0-9]+),\s*Min:\s*([0-9\.]+),\s*Max:\s*([0-9\.]+)$"
    match = re.match(pattern, content)
    assert match is not None, f"File {path} content '{content}' does not match the expected format 'Unique: <N>, Min: <val>, Max: <val>'."

    unique_count = int(match.group(1))
    assert unique_count > 1, f"Expected non-deterministic output with Unique > 1, but got {unique_count}."

def test_stable_score_output():
    path = "/home/user/stable_score.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run fix_sim.sh?"

    with open(path, "r") as f:
        content = f.read().strip()

    pattern = r"^Stable Score:\s*([0-9\.]+)$"
    match = re.match(pattern, content)
    assert match is not None, f"File {path} content '{content}' does not match the expected format 'Stable Score: <val>'."