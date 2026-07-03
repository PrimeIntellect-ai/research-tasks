# test_final_state.py

import os
import pytest

def test_recovered_admin_token():
    token_file = "/home/user/recovered_admin_token.txt"
    assert os.path.isfile(token_file), f"The output file {token_file} does not exist."

    with open(token_file, "r") as f:
        content = f.read()

    expected_token = "super_secret_token_99"
    assert content == expected_token, (
        f"The recovered token is incorrect. "
        f"Expected exactly {repr(expected_token)} (no newlines), but got {repr(content)}."
    )