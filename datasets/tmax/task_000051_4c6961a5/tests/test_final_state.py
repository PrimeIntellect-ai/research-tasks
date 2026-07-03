# test_final_state.py

import os
import pytest

def is_valid_token(token: str) -> bool:
    h = 0
    p = 31
    m = int(1e9 + 9)
    p_pow = 1
    for char in token:
        h = (h + (ord(char) - ord('a') + 1) * p_pow) % m
        p_pow = (p_pow * p) % m
    return h % 1337 == 42

def test_static_library_built():
    lib_path = "/home/user/websec_port/libpolyhash.a"
    assert os.path.isfile(lib_path), f"The C static library was not built at {lib_path}"

def test_valid_tokens_file_exists():
    out_path = "/home/user/websec_port/valid_tokens.txt"
    assert os.path.isfile(out_path), f"The output file {out_path} was not created"

def test_valid_tokens_content():
    tokens_path = "/home/user/websec_port/tokens.txt"
    out_path = "/home/user/websec_port/valid_tokens.txt"

    assert os.path.isfile(tokens_path), f"Input file {tokens_path} is missing"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing"

    expected_tokens = []
    with open(tokens_path, "r") as f:
        for line in f:
            token = line.strip()
            if token and is_valid_token(token):
                expected_tokens.append(token)

    expected_tokens.sort()

    actual_tokens = []
    with open(out_path, "r") as f:
        for line in f:
            token = line.strip()
            if token:
                actual_tokens.append(token)

    actual_tokens.sort()

    assert actual_tokens == expected_tokens, "The valid_tokens.txt file does not contain the correct valid tokens."