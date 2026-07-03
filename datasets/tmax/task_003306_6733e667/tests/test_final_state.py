# test_final_state.py

import os
from pathlib import Path

def test_recovered_data_file():
    recovered_file = Path("/home/user/recovered.dat")
    assert recovered_file.exists(), "/home/user/recovered.dat does not exist."

    with open(recovered_file, "rb") as f:
        content = f.read()

    expected_content = b'\x04test\x05hello\x06urgent'
    assert content == expected_content, f"Content of /home/user/recovered.dat is incorrect. Expected {expected_content}, got {content}"

def test_final_metrics_output():
    final_file = Path("/home/user/final_metrics.txt")
    assert final_file.exists(), "/home/user/final_metrics.txt does not exist."

    with open(final_file, "r") as f:
        content = f.read()

    expected_content = "test,hello,urgent\n"
    assert content == expected_content, f"Content of /home/user/final_metrics.txt is incorrect. Expected {repr(expected_content)}, got {repr(content)}"

def test_rust_parser_fixed():
    main_rs = Path("/home/user/parser/src/main.rs")
    assert main_rs.exists(), "/home/user/parser/src/main.rs does not exist."

    with open(main_rs, "r") as f:
        content = f.read()

    # The original buggy line was: let mut buf = vec![0u8; len + 1];
    # We should ensure the off-by-one error is fixed.
    assert "len + 1" not in content or "buf.len(), len" not in content or "vec![0u8; len]" in content, "The buffer allocation bug in /home/user/parser/src/main.rs does not appear to be fixed."