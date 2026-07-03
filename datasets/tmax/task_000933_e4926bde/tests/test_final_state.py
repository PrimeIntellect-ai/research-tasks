# test_final_state.py
import os

def test_flag_file_exists():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"The file {flag_path} does not exist. Did your program write to it?"
    assert os.path.isfile(flag_path), f"{flag_path} is not a regular file."

def test_flag_content():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"Cannot check content because {flag_path} does not exist."

    with open(flag_path, "r") as f:
        content = f.read()

    expected_flag = "FLAG{JWT_byp4ss_r3c0v3ry}"
    assert expected_flag in content, f"The file {flag_path} does not contain the correct flag. Found: {content.strip()}"

def test_recover_rust_code_exists():
    standalone_path = "/home/user/recover.rs"
    cargo_path = "/home/user/recover/src/main.rs"

    assert os.path.exists(standalone_path) or os.path.exists(cargo_path), \
        "Could not find the Rust program at /home/user/recover.rs or /home/user/recover/src/main.rs"