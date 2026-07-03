# test_final_state.py
import os

def test_clean_dataset_exists_and_content():
    expected_content = """record_id,scaled_measurement
102,450.0
103,220.0
105,123.0
108,5.0"""

    file_path = "/home/user/clean_dataset.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\nGot:\n{content}"
    )

def test_script_exists_and_uses_atomic_write():
    script_path = "/home/user/compile_results.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for atomic rename mechanisms
    has_rename = any(func in content for func in ["os.rename", "os.replace", "shutil.move"])
    assert has_rename, "Script does not appear to use an atomic rename operation (e.g., os.rename, os.replace, or shutil.move)."

    has_tmp = ".tmp" in content or "temp" in content.lower() or "NamedTemporaryFile" in content
    assert has_tmp, "Script does not appear to use a temporary file for atomic writing."