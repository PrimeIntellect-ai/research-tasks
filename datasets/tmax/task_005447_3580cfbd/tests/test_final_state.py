# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_bad_commit_hash():
    """Check if the student identified the correct bad commit."""
    truth_file = "/tmp/.truth_bad_commit"
    student_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(student_file), f"File {student_file} does not exist."

    with open(truth_file, "r") as f:
        truth_hash = f.read().strip()

    with open(student_file, "r") as f:
        student_hash = f.read().strip()

    assert student_hash == truth_hash, f"The commit hash in {student_file} is incorrect. Expected {truth_hash}, got {student_hash}."

def test_fixed_script_exists_and_executable():
    """Check if the fixed script exists and is executable."""
    script_path = "/home/user/fixed_process_metrics.sh"
    assert os.path.isfile(script_path), f"Fixed script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Fixed script {script_path} is not executable."

def test_fixed_script_handles_edge_case():
    """Check if the fixed script successfully processes the edge case (all zeros)."""
    script_path = "/home/user/fixed_process_metrics.sh"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tf:
        tf.write("1,active,0\n2,active,0\n")
        tf_path = tf.name

    try:
        result = subprocess.run([script_path, tf_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on edge case data (all zeros). Exit code: {result.returncode}, Stderr: {result.stderr}"
    finally:
        os.remove(tf_path)

def test_fixed_script_handles_normal_case():
    """Check if the fixed script successfully processes normal data."""
    script_path = "/home/user/fixed_process_metrics.sh"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tf:
        tf.write("1,active,100\n2,active,200\n")
        tf_path = tf.name

    try:
        result = subprocess.run([script_path, tf_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on normal data. Exit code: {result.returncode}, Stderr: {result.stderr}"
    finally:
        os.remove(tf_path)