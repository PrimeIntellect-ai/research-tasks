# test_final_state.py
import os
import subprocess

def test_kv_store_cpp_fixed():
    path = "/home/user/kv_store/kv_store.cpp"
    assert os.path.isfile(path), f"{path} is missing"

    with open(path, "r") as f:
        content = f.read()

    assert "void KVStore::put" in content, "put method missing in kv_store.cpp"

    # Extract the body of the put method
    # Assuming standard ordering where get comes after put, or just check the whole file if get is before put.
    # To be robust, let's just check if 'lock' or 'mtx' is used anywhere after 'void KVStore::put'
    put_section = content.split("void KVStore::put")[1]

    # We look for typical locking mechanisms in the put method
    assert "lock" in put_section or "mtx" in put_section, "No lock or mutex usage found in KVStore::put method."

def test_recovered_data():
    path = "/home/user/recovered_data.txt"
    assert os.path.isfile(path), f"{path} is missing"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["foo=bar", "hello=world", "test=123"]
    assert lines == expected, f"Content of {path} does not match the expected sorted entries. Got: {lines}"

def test_race_script_execution():
    path = "/home/user/test_race.sh"
    assert os.path.isfile(path), f"{path} is missing"

    # Run the script and verify it exits with 0
    result = subprocess.run(["bash", path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"{path} failed with exit code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"