# test_final_state.py

import os

def test_decoded_message_exists_and_correct():
    out_file = "/home/user/decoded_message.txt"
    assert os.path.isfile(out_file), f"Output file {out_file} does not exist. Did you save the standard output of run.sh?"

    with open(out_file, "r") as f:
        content = f.read()

    assert content == "CORRECT\n", f"The decoded message in {out_file} is incorrect. Expected 'CORRECT\\n', got {repr(content)}"

def test_interpreter_binary_exists():
    bin_file = "/home/user/repo/interpreter_bin"
    assert os.path.isfile(bin_file), f"Interpreter binary {bin_file} does not exist. Did you successfully compile the Rust code using build.sh?"
    assert os.access(bin_file, os.X_OK), f"Interpreter binary {bin_file} is not executable."