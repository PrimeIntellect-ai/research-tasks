# test_final_state.py
import os

def test_flag_extracted():
    flag_path = "/home/user/flag.txt"

    # Check if the flag file was created
    assert os.path.exists(flag_path), f"Expected {flag_path} to exist. The script did not run successfully or did not write the output."
    assert os.path.isfile(flag_path), f"Expected {flag_path} to be a file."

    # Verify the contents of the flag file
    with open(flag_path, "r") as f:
        flag_content = f.read().strip()

    expected_flag = "FLAG{fL0at1ng_p0int_f0r3ns1cs_M4st3r}"
    assert flag_content == expected_flag, f"Expected the flag to be '{expected_flag}', but got '{flag_content}'. Ensure the script correctly extracts the flag from the database."