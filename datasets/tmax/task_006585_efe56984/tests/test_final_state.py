# test_final_state.py
import os

def test_cpp_source_exists():
    """Verify that the C++ source file was created."""
    src_path = "/home/user/artifact_tracker.cpp"
    assert os.path.isfile(src_path), f"The C++ source file {src_path} was not found."

def test_output_file_exists_and_content():
    """Verify that the output file exists and contains the correct results."""
    output_path = "/home/user/best_experiment.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you compile and run the C++ program?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected = "Closest Exp: e2, Distance: 0.1414, Acc_Test_Pass: false"
    assert content == expected, f"Output file content mismatch.\nExpected: '{expected}'\nGot: '{content}'"