# test_final_state.py

import os
import ast

def test_extracted_comments_file_exists():
    output_file = "/home/user/extracted_comments.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

def test_extracted_comments_content():
    output_file = "/home/user/extracted_comments.txt"
    expected_lines = [
        "Begin finishing pass",
        "Cut at 45° angle",
        "End of job",
        "Initialize spindlé"
    ]

    try:
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read().splitlines()
    except UnicodeDecodeError:
        assert False, f"Output file {output_file} is not properly encoded in UTF-8."

    assert content == expected_lines, f"Content of {output_file} does not match expected output. Got: {content}"

def test_script_exists_and_uses_atomic_write():
    script_file = "/home/user/extract.py"
    assert os.path.isfile(script_file), f"Script file {script_file} does not exist."

    with open(script_file, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Check for atomic write functions
    valid_atomic_funcs = ["os.replace", "os.rename", "shutil.move"]
    has_atomic = any(func in script_content for func in valid_atomic_funcs)
    assert has_atomic, f"Script {script_file} does not appear to use an atomic write method (os.replace, os.rename, or shutil.move)."

def test_script_has_symlink_cycle_detection():
    script_file = "/home/user/extract.py"
    with open(script_file, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Simple check for realpath or similar cycle detection logic
    # The requirement says "contains symlink cycle detection logic (e.g. tracking os.path.realpath in a set)"
    has_realpath = "realpath" in script_content or "abspath" in script_content or "samefile" in script_content
    has_set_or_dict = "set()" in script_content or "{" in script_content or "dict" in script_content or "[]" in script_content

    assert has_realpath and has_set_or_dict, f"Script {script_file} does not appear to contain cycle detection logic tracking visited paths."