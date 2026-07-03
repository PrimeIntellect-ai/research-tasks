# test_final_state.py
import os

def test_ws_mock_script_exists():
    """Verify that the WebSocket mock server script exists."""
    filepath = "/home/user/ws_mock.py"
    assert os.path.isfile(filepath), f"Expected server script at {filepath} does not exist."

def test_client_script_exists():
    """Verify that the WebSocket client script exists."""
    filepath = "/home/user/client.py"
    assert os.path.isfile(filepath), f"Expected client script at {filepath} does not exist."

def test_ws_output_correct():
    """Verify that the output file exists and contains the correct evaluated result."""
    filepath = "/home/user/ws_output.txt"
    assert os.path.isfile(filepath), f"Expected output file at {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_output = "22.0"
    assert content == expected_output, (
        f"Output file {filepath} content is incorrect. "
        f"Expected '{expected_output}', but got '{content}'."
    )