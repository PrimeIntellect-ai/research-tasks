# test_final_state.py
import os
import json
import hashlib

def test_organize_script_exists():
    assert os.path.isfile("/home/user/organize.py"), "/home/user/organize.py does not exist."

def test_safe_files_extracted():
    safe_doc = "/home/user/backup/safe_doc.txt"
    app_py = "/home/user/backup/src/app.py"

    assert os.path.isfile(safe_doc), f"{safe_doc} does not exist."
    with open(safe_doc, "r") as f:
        assert f.read() == "This is a safe file.", f"Content of {safe_doc} is incorrect."

    assert os.path.isfile(app_py), f"{app_py} does not exist."
    with open(app_py, "r") as f:
        assert f.read() == 'print("Hello World")', f"Content of {app_py} is incorrect."

def test_malicious_files_not_extracted():
    assert not os.path.exists("/home/user/backup/evil.sh"), "evil.sh was extracted into backup dir!"
    assert not os.path.exists("/home/user/backup/another_evil.txt"), "another_evil.txt was extracted into backup dir!"
    assert not os.path.exists("/evil.sh"), "evil.sh was extracted to the root directory!"

def test_skipped_log():
    log_path = "/home/user/skipped.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "../../../evil.sh" in lines, "../../../evil.sh missing from skipped.log"
    assert "folder/../../another_evil.txt" in lines, "folder/../../another_evil.txt missing from skipped.log"
    assert len(lines) == 2, f"skipped.log contains unexpected entries: {lines}"

def test_state_json():
    state_path = "/home/user/state.json"
    assert os.path.isfile(state_path), f"{state_path} does not exist."

    with open(state_path, "r") as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError:
            assert False, "state.json is not valid JSON."

    expected_safe_doc_md5 = hashlib.md5(b"This is a safe file.").hexdigest()
    expected_app_py_md5 = hashlib.md5(b'print("Hello World")').hexdigest()

    assert state.get("safe_doc.txt") == expected_safe_doc_md5, "MD5 for safe_doc.txt is missing or incorrect in state.json."
    assert state.get("src/app.py") == expected_app_py_md5, "MD5 for src/app.py is missing or incorrect in state.json."

def test_script_contains_required_functions():
    script_path = "/home/user/organize.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, "Script does not use fcntl.flock as required."
    assert "os.replace" in content, "Script does not use os.replace as required."
    assert "os.fsync" in content, "Script does not use os.fsync as required."