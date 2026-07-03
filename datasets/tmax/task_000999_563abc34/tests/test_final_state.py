# test_final_state.py
import os

def test_cholesky_diags_output():
    """Check that the output file exists and contains the correct traces."""
    output_file = "/home/user/cholesky_diags.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected_content = "15.908070,15.908070"
    assert content == expected_content, f"Expected output '{expected_content}', but got '{content}'."

def test_script_exists():
    """Check that the script file was created."""
    script_file = "/home/user/prepare_data.py"
    assert os.path.exists(script_file), f"Script file {script_file} does not exist."