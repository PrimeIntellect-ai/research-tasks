# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/ticket_4092"

def test_resolution_txt():
    res_path = os.path.join(BASE_DIR, "resolution.txt")
    assert os.path.isfile(res_path), f"Resolution output file missing: {res_path}"

    with open(res_path, "r") as f:
        content = f.read().strip()

    assert content == "Result: 192", f"Expected output 'Result: 192', but got '{content}'"

def test_parser_rs_recovered():
    parser_path = os.path.join(BASE_DIR, "repo", "src", "parser.rs")
    assert os.path.isfile(parser_path), f"Recovered file missing: {parser_path}"

    with open(parser_path, "r") as f:
        content = f.read()

    assert "pub fn process_data(data: &[u8], start: usize, end: usize) -> u32" in content, "parser.rs does not contain the expected function signature."
    assert "crate::compute_checksum" in content, "parser.rs does not contain the expected checksum call."

def test_main_rs_fixed():
    main_path = os.path.join(BASE_DIR, "repo", "src", "main.rs")
    assert os.path.isfile(main_path), f"File missing: {main_path}"

    with open(main_path, "r") as f:
        content = f.read()

    assert "data.len() - 1" not in content, "main.rs still contains the off-by-one error (data.len() - 1)."
    assert "parser::process_data(&data, 0, data.len())" in content.replace(" ", ""), "main.rs does not call process_data with the correct bounds."