# test_final_state.py

import os
import subprocess

def test_final_output_exists():
    """Check if the final_output.txt file was created."""
    assert os.path.isfile("/home/user/pcap_parser/final_output.txt"), (
        "The file /home/user/pcap_parser/final_output.txt does not exist. "
        "Did you save the output of your program?"
    )

def test_final_output_content():
    """Verify that the final output exactly matches the expected output."""
    expected_path = "/home/user/pcap_parser/expected_output.txt"
    final_path = "/home/user/pcap_parser/final_output.txt"

    assert os.path.isfile(expected_path), f"Expected output file {expected_path} is missing."

    with open(expected_path, "r") as f:
        expected_content = f.read()

    with open(final_path, "r") as f:
        final_content = f.read()

    assert final_content == expected_content, (
        "The content of final_output.txt does not match expected_output.txt. "
        "Check your C++ payload extraction logic."
    )

def test_parser_binary_exists():
    """Check if the parser binary was successfully built."""
    assert os.path.isfile("/home/user/pcap_parser/parser"), (
        "The compiled binary '/home/user/pcap_parser/parser' is missing. "
        "Did you fix the Makefile and successfully run 'make'?"
    )
    assert os.access("/home/user/pcap_parser/parser", os.X_OK), (
        "The file '/home/user/pcap_parser/parser' is not executable."
    )