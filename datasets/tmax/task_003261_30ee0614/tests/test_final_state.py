# test_final_state.py
import os
import subprocess
import base64

def test_bad_commit_identified():
    student_file = "/home/user/bad_commit.txt"
    truth_file = "/home/user/truth_bad_commit.txt"

    assert os.path.isfile(student_file), f"File {student_file} does not exist."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} does not exist."

    with open(student_file, "r") as f:
        student_commit = f.read().strip()

    with open(truth_file, "r") as f:
        truth_commit = f.read().strip()

    assert student_commit == truth_commit, f"Expected bad commit {truth_commit}, but got {student_commit}."

def test_fixed_output_matches_expected():
    student_output_file = "/home/user/fixed_output.txt"
    truth_output_file = "/home/user/expected_output_truth.txt"

    assert os.path.isfile(student_output_file), f"File {student_output_file} does not exist."
    assert os.path.isfile(truth_output_file), f"Truth file {truth_output_file} does not exist."

    with open(student_output_file, "r") as f:
        student_output = f.read().strip()

    with open(truth_output_file, "r") as f:
        truth_output = f.read().strip()

    assert student_output == truth_output, "The contents of fixed_output.txt do not match the expected correct output."

def test_processor_script_fixed():
    processor_path = "/home/user/project/processor.py"
    data_path = "/home/user/data.bin"

    assert os.path.isfile(processor_path), f"File {processor_path} does not exist."
    assert os.path.isfile(data_path), f"File {data_path} does not exist."

    # Run the current processor.py on data.bin and check if it produces the correct output
    try:
        result = subprocess.run(
            ["python3", processor_path, data_path],
            capture_output=True,
            text=True,
            check=True
        )
        current_output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        assert False, f"Running processor.py failed: {e.stderr}"

    truth_output_file = "/home/user/expected_output_truth.txt"
    with open(truth_output_file, "r") as f:
        truth_output = f.read().strip()

    assert current_output == truth_output, "The processor.py script in the working tree still produces incorrect output. It has not been fixed properly."