# test_final_state.py

import os
import pytest

def test_recovered_token_file():
    token_path = "/home/user/recovered_token.txt"
    assert os.path.isfile(token_path), f"File {token_path} does not exist."
    with open(token_path, "r") as f:
        content = f.read().strip()
    assert content == "sre_token_99x21", f"Expected token 'sre_token_99x21', but found '{content}'."

def test_monitor_output_file():
    output_path = "/home/user/monitor_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist."
    with open(output_path, "r") as f:
        content = f.read()
    assert "SLA Status: 99.999% OK" in content, "The monitor output does not contain the expected SLA status message."

def test_monitor_c_modified():
    monitor_c_path = "/home/user/uptime_monitor/monitor.c"
    assert os.path.isfile(monitor_c_path), f"File {monitor_c_path} does not exist."
    with open(monitor_c_path, "r") as f:
        content = f.read()

    # The original file had a specific bug with float precision. 
    # If the user fixed it, they likely changed float to double, or changed the loop condition.
    # We check if the original exact buggy line is gone or modified.
    original_buggy_declaration = "float uptime_seconds = 16777210.0f;"
    original_target_declaration = "float target_uptime = 16777220.0f;"

    # If both exact lines are still there and it's still using floats without casting, it might still be buggy.
    # However, just checking that the file is not exactly the original is a good start.
    # The output file test already proves the program terminated successfully.
    # Let's just ensure it's not the exact original buggy file.
    original_content_snippet = "float uptime_seconds = 16777210.0f;\n    float target_uptime = 16777220.0f;"

    # It's possible the user changed the types to double or modified the increment.
    # We will assert that the file has been modified to fix the bug.
    is_original = original_content_snippet in content and "uptime_seconds += 1.0f;" in content

    assert not is_original, "The monitor.c file appears to be unmodified and still contains the infinite loop bug."