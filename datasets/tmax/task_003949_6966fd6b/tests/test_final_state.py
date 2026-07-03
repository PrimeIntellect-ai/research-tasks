# test_final_state.py

import os
import stat

def test_run_analysis_exists_and_executable():
    path = "/home/user/run_analysis.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {path} is not executable."

def test_metric_txt_content():
    path = "/home/user/metric.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "2", f"Expected metric.txt to contain exactly '2', but got '{content}'."