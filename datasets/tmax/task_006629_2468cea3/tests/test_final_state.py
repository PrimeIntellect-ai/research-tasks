# test_final_state.py

import os
import subprocess
import pytest

def test_output_file_exists_and_correct():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run the script?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "1000", f"Expected output.txt to contain '1000', but found '{content}'."

def test_pandas_version_downgraded():
    result = subprocess.run(["pip", "show", "pandas"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run pip show pandas."

    version_line = next((line for line in result.stdout.split('\n') if line.startswith('Version:')), None)
    assert version_line is not None, "Could not find Version in pip show pandas output."

    version = version_line.split(' ')[1]
    major_version = int(version.split('.')[0])
    assert major_version < 2, f"Expected pandas version < 2.0.0, but found {version}."

def test_process_script_fixes():
    path = "/home/user/process.py"
    assert os.path.isfile(path), f"Script {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Requirement: Do not modify the two pandas-related lines
    assert "df.append(" in content, "You modified or removed the df.append line, which was forbidden."
    assert "pd.DataFrame()" in content, "You modified or removed the pd.DataFrame() line, which was forbidden."

    # Check for thread synchronization mechanism
    has_lock = any(lock_term in content for lock_term in ["Lock()", "RLock()", "Semaphore", "Mutex"])
    assert has_lock, "Could not find a thread synchronization mechanism (like threading.Lock()) in process.py."

    # Check for some form of json cleaning or trailing comma handling
    # The student could do line.replace(',}', '}'), re.sub, or replace(',\n', '\n') etc.
    # We just ensure the output is 1000, but we can also check if they modified the json.loads line or line content.
    assert "json.loads" in content, "Expected json.loads to still be used in process.py"