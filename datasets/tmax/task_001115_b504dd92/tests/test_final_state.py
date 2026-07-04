# test_final_state.py
import os
import pytest

def test_secret_key_recovered():
    key_file = "/home/user/secret_key.txt"
    assert os.path.isfile(key_file), f"Secret key file not found at {key_file}"

    with open(key_file, "r") as f:
        content = f.read().strip()

    assert content == "A1B2C3D4E5F67890", f"Secret key file contains incorrect key: {content}"

def test_final_output_exists_and_correct():
    output_file = "/home/user/final_output.txt"
    assert os.path.isfile(output_file), f"Final output file not found at {output_file}"

    with open(output_file, "r") as f:
        content = f.read()

    # Check for the decrypted payloads
    assert "DEADBEEF" in content, "Final output does not contain the decrypted payload for Chunk 1 (DEADBEEF)"
    assert "1122" in content, "Final output does not contain the decrypted payload for Chunk 3 (1122)"

    # Ensure the output is in the correct order
    idx1 = content.find("DEADBEEF")
    idx2 = content.find("1122")
    assert idx1 < idx2, "Decrypted payloads are not in the expected order in the output file"