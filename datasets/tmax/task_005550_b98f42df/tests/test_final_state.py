# test_final_state.py
import os
import json
import ast
import pytest

def test_bad_file_log():
    log_path = "/home/user/bad_file.log"
    assert os.path.exists(log_path), f"File {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "file_387.txt", f"Expected 'file_387.txt' in {log_path}, got '{content}'"

def test_mre_py():
    mre_path = "/home/user/mre.py"
    assert os.path.exists(mre_path), f"File {mre_path} is missing."
    with open(mre_path, "r") as f:
        content = f.read()

    # Check that it opens the bad file
    assert "file_387.txt" in content, "mre.py does not reference the corrupt file 'file_387.txt'."

    # Check that running it raises UnicodeDecodeError
    # We will just execute it in a safe way or check if it crashes.
    # The prompt says: "triggers the exact underlying UnicodeDecodeError"
    import subprocess
    result = subprocess.run(["python3", mre_path], capture_output=True, text=True)
    assert result.returncode != 0, "mre.py should crash with an error, but it exited successfully."
    assert "UnicodeDecodeError" in result.stderr, "mre.py did not trigger a UnicodeDecodeError."

def test_build_py_fixed():
    build_path = "/home/user/project/build.py"
    assert os.path.exists(build_path), f"File {build_path} is missing."
    with open(build_path, "r") as f:
        content = f.read()

    # Check for encoding and errors arguments in the open call
    assert "errors=" in content and ("'replace'" in content or '"replace"' in content), "build.py does not contain errors='replace'."
    assert "encoding=" in content and ("'utf-8'" in content or '"utf-8"' in content or "'utf8'" in content or '"utf8"' in content), "build.py does not contain encoding='utf-8'."

def test_output_json():
    output_path = "/home/user/project/output.json"
    assert os.path.exists(output_path), f"File {output_path} is missing. Did you run build.py?"

    with open(output_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    # Check for the bad file key
    key = "data/file_387.txt"
    # The script might use absolute paths or relative paths depending on how it was run, but original script uses "data/*.txt"
    # Let's check for any key ending with file_387.txt
    matching_keys = [k for k in data.keys() if k.endswith("file_387.txt")]
    assert matching_keys, "output.json does not contain a key for file_387.txt."

    val = data[matching_keys[0]]
    assert "\ufffd" in val, "The value for file_387.txt does not contain the replacement character \\ufffd."