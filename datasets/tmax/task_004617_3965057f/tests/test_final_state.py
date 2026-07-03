# test_final_state.py
import os

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"The flag file {flag_path} was not created. Did you successfully exploit the binary?"
    assert os.path.isfile(flag_path), f"{flag_path} is not a regular file."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{rust_jwt_alg_none_exploited_992}"
    assert content == expected_flag, f"The content of {flag_path} is incorrect. Expected {expected_flag}, but got {content}."

def test_craft_token_rs_exists():
    craft_path = "/home/user/craft_token.rs"
    assert os.path.exists(craft_path), f"The exploit source file {craft_path} does not exist."
    assert os.path.isfile(craft_path), f"{craft_path} is not a regular file."

    with open(craft_path, "r") as f:
        content = f.read()

    assert "fn main" in content, f"{craft_path} does not appear to contain valid Rust code (missing 'fn main')."