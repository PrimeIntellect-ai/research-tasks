# test_final_state.py

import os

def test_exploit_script_exists():
    """
    Verifies that the student has created the exploit script at the required location.
    """
    exploit_path = "/home/user/exploit.py"
    assert os.path.exists(exploit_path), f"Exploit script was not found at {exploit_path}. You must save your script here."
    assert os.path.isfile(exploit_path), f"The path {exploit_path} exists but is not a file."

def test_extracted_flag_matches():
    """
    Verifies that the extracted flag file exists and its contents perfectly match the original secret flag.
    This confirms the exploit successfully bypassed the WAF and executed the RCE payload.
    """
    flag_path = "/home/user/flag.txt"
    extracted_flag_path = "/home/user/extracted_flag.txt"

    assert os.path.exists(flag_path), f"The original flag file {flag_path} is missing. The environment may be corrupted."
    assert os.path.exists(extracted_flag_path), f"The extracted flag file was not found at {extracted_flag_path}. The exploit may have failed to execute or write the file."
    assert os.path.isfile(extracted_flag_path), f"The path {extracted_flag_path} exists but is not a file."

    with open(flag_path, 'r') as f:
        expected_contents = f.read()

    with open(extracted_flag_path, 'r') as f:
        extracted_contents = f.read()

    assert extracted_contents == expected_contents, (
        "The contents of the extracted flag do not match the original flag. "
        "Ensure your exploit is reading the exact contents and writing them without modification."
    )