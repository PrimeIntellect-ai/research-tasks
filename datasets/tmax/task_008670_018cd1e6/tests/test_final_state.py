# test_final_state.py
import os

def test_final_output_file():
    """
    Verifies that the final output file exists and contains the correct base32 encoded string
    for the prime factors of 314159265.
    """
    output_file = "/home/user/final_output.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist. The script might not have been run or failed."

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_content = "GMYDQNDFEQ3DMMJTGMZTI==="
    assert content == expected_content, f"Expected base32 string '{expected_content}', got '{content}'. Check the math and encoding logic."