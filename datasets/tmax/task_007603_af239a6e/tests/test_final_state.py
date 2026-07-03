# test_final_state.py
import os
import re

def test_report_exists():
    """Check if the report file was created."""
    assert os.path.isfile("/home/user/report.txt"), "/home/user/report.txt is missing. Did you save the output?"

def test_report_content():
    """Check if the report contains the correct optimal alpha and MSE."""
    with open("/home/user/report.txt", "r") as f:
        content = f.read().strip()

    expected_pattern = r"Optimal alpha:\s*0\.37,\s*Best CV MSE:\s*0\.334057"
    match = re.search(expected_pattern, content)

    assert match is not None, (
        f"The output in /home/user/report.txt is incorrect.\n"
        f"Expected it to match: 'Optimal alpha: 0.37, Best CV MSE: 0.334057'\n"
        f"Actual content: '{content}'"
    )

def test_c_code_fixed():
    """Verify that the C code was modified to fix the data schema bug."""
    assert os.path.isfile("/home/user/etl_pipeline.c"), "/home/user/etl_pipeline.c is missing."
    with open("/home/user/etl_pipeline.c", "r") as f:
        content = f.read()

    assert "float id;" not in content, "The C code still contains 'float id;'. The ID field must be changed to an unsigned 64-bit integer type."

def test_binary_exists():
    """Check if the compiled binary exists."""
    assert os.path.isfile("/home/user/etl_pipeline"), "The compiled binary /home/user/etl_pipeline is missing. Did you compile the C code?"
    assert os.access("/home/user/etl_pipeline", os.X_OK), "/home/user/etl_pipeline is not executable."