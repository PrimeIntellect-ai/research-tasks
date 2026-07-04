# test_final_state.py

import os
import subprocess
import re

def test_bad_commit_identified():
    truth_file = "/tmp/true_bad_commit.txt"
    student_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(student_file), f"File {student_file} is missing."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing."

    with open(truth_file, "r") as f:
        true_commit = f.read().strip()

    with open(student_file, "r") as f:
        student_commit = f.read().strip()

    assert student_commit == true_commit, f"Expected commit hash {true_commit}, but got {student_commit} in {student_file}"

def test_parser_fixed():
    parser_file = "/home/user/netdaemon/parser.c"
    assert os.path.isfile(parser_file), f"{parser_file} is missing."

    # We can use the provided test_hang.sh to verify it doesn't hang
    script_path = "/home/user/netdaemon/test_hang.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."

    result = subprocess.run(["bash", script_path], cwd="/home/user/netdaemon", capture_output=True)
    assert result.returncode == 0, "The daemon still hangs on malformed packets. Ensure parser.c prevents infinite recursion."

def test_worker_fixed():
    worker_file = "/home/user/netdaemon/worker.c"
    assert os.path.isfile(worker_file), f"{worker_file} is missing."

    with open(worker_file, "r") as f:
        content = f.read()

    assert "pthread_mutex_lock" in content and "stats_mutex" in content, "worker.c is missing pthread_mutex_lock for stats_mutex"
    assert "pthread_mutex_unlock" in content and "stats_mutex" in content, "worker.c is missing pthread_mutex_unlock for stats_mutex"

def test_final_output():
    output_file = "/home/user/final_output.txt"
    assert os.path.isfile(output_file), f"File {output_file} is missing. Did you run the daemon and redirect output?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert "Total bytes: 24" in content, f"Expected 'Total bytes: 24' in {output_file}, but got: {content}"