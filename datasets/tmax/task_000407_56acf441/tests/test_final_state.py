# test_final_state.py
import os

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"The file {flag_path} does not exist."
    assert os.path.isfile(flag_path), f"{flag_path} is not a file."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{csp_and_cookies_reversed}"
    assert content == expected_flag, f"The content of {flag_path} is incorrect. Expected '{expected_flag}', got '{content}'."

def test_exploit_cpp_exists():
    exploit_path = "/home/user/exploit.cpp"
    assert os.path.exists(exploit_path), f"The C++ source file {exploit_path} does not exist."
    assert os.path.isfile(exploit_path), f"{exploit_path} is not a file."