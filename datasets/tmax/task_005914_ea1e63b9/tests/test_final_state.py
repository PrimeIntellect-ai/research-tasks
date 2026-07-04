# test_final_state.py
import os
import pytest

def test_pipeline_cpp_exists():
    """Verify that the C++ source file was created."""
    assert os.path.isfile('/home/user/pipeline.cpp'), "The C++ source file /home/user/pipeline.cpp is missing."

def test_model_results_exists():
    """Verify that the output file was generated."""
    assert os.path.isfile('/home/user/model_results.txt'), "The output file /home/user/model_results.txt is missing. Did you compile and run the program?"

def test_model_results_content():
    """Verify that the output file contains the correct calculated values formatted properly."""
    expected_lines = [
        "m: 2.5000",
        "b: 1.2000",
        "MAE: 0.0000"
    ]

    with open('/home/user/model_results.txt', 'r') as f:
        content = f.read().strip().split('\n')

    # Remove any trailing empty lines
    content = [line.strip() for line in content if line.strip()]

    assert len(content) == 3, f"Expected exactly 3 lines in model_results.txt, but got {len(content)}."

    for i, expected in enumerate(expected_lines):
        assert content[i] == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{content[i]}'."