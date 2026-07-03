# test_final_state.py
import os

EXPECTED_CONTENT = """[ERROR] 2023-01-01 10:00:10 Failed to load config
  Line 1: missing semicolon
  Line 2: invalid syntax
  File "config.xml", line 42
[ERROR] 2023-01-02 11:30:00 NullPointerException
  at module.main(Main.java:42)
  at system.run(System.java:10)
"""

def test_extracted_errors_file_exists():
    path = "/home/user/extracted_errors.log"
    assert os.path.isfile(path), f"File {path} does not exist. Make sure you extracted the errors to the correct location."

def test_extracted_errors_content():
    path = "/home/user/extracted_errors.log"
    if not os.path.isfile(path):
        return  # Handled by previous test

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        assert False, f"File {path} is not valid UTF-8. Ensure you converted the encoding from UTF-16LE to UTF-8."

    assert content == EXPECTED_CONTENT, "The extracted errors do not match the expected content exactly. Ensure multi-line records are handled correctly."