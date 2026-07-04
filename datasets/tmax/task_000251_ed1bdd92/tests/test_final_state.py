# test_final_state.py

import os
import pytest

def test_student_scripts_exist():
    """Verify that the student created the required script and C++ source files."""
    assert os.path.exists("/home/user/analyze_audit.sh"), "Required shell script /home/user/analyze_audit.sh does not exist."
    assert os.path.exists("/home/user/detector.cpp"), "Required C++ source file /home/user/detector.cpp does not exist."

def test_peak_frame_result():
    """Verify that the peak frame index is within the acceptable threshold."""
    output_file = "/home/user/peak_frame.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist. The C++ program may not have run successfully."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        predicted_frame = int(content)
    except ValueError:
        pytest.fail(f"File {output_file} does not contain a valid integer. Found: '{content}'")

    target_frame = 142
    threshold = 2
    error = abs(predicted_frame - target_frame)

    assert error <= threshold, (
        f"Predicted frame {predicted_frame} is outside the acceptable threshold of {threshold} "
        f"from the target {target_frame}. Absolute error: {error}"
    )