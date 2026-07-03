# test_final_state.py

import os

def test_bad_commit_identified():
    student_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(student_file), f"The file {student_file} does not exist. Did you find the bad commit?"
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing."

    with open(student_file, "r") as sf:
        student_commit = sf.read().strip()

    with open(truth_file, "r") as tf:
        truth_commit = tf.read().strip()

    assert student_commit != "", "The file /home/user/bad_commit.txt is empty."
    assert student_commit == truth_commit, f"The commit hash in {student_file} is incorrect. Expected {truth_commit}, got {student_commit}."

def test_minimal_crash_extracted():
    student_file = "/home/user/minimal_crash.bin"
    truth_file = "/tmp/expected_minimal.bin"

    assert os.path.isfile(student_file), f"The file {student_file} does not exist. Did you extract the minimal crash payload?"
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing."

    with open(student_file, "rb") as sf:
        student_data = sf.read()

    with open(truth_file, "rb") as tf:
        truth_data = tf.read()

    assert len(student_data) > 0, "The file /home/user/minimal_crash.bin is empty."
    assert student_data == truth_data, (
        f"The content of {student_file} does not match the expected minimal TLV record. "
        f"Expected {truth_data.hex()}, got {student_data.hex()}."
    )