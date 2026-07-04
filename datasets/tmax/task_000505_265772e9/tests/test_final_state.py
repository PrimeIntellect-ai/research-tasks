# test_final_state.py
import os
import sys
import pytest

APP_DIR = "/home/user/app"
RESULTS_FILE = os.path.join(APP_DIR, "results.txt")
MAIN_FILE = os.path.join(APP_DIR, "main.py")
SETUP_FILE = os.path.join(APP_DIR, "setup.py")
STREAM_LOG = os.path.join(APP_DIR, "stream.log")

def test_main_py_exists():
    assert os.path.isfile(MAIN_FILE), f"{MAIN_FILE} does not exist. You must implement the Python script."

def test_setup_py_fixed():
    assert os.path.isfile(SETUP_FILE), f"{SETUP_FILE} does not exist."
    with open(SETUP_FILE, "r") as f:
        content = f.read()

    # Check if runtime_library_dirs or extra_link_args with rpath is used
    has_rpath = "runtime_library_dirs" in content or "-Wl,-rpath" in content
    assert has_rpath, "setup.py does not appear to permanently encode the library path (e.g., using runtime_library_dirs)."

def test_extension_import_and_execution():
    # Attempt to import the built extension
    sys.path.insert(0, APP_DIR)
    try:
        import _legacy_wrapper
    except ImportError as e:
        pytest.fail(f"Failed to import _legacy_wrapper. Is the linking issue fixed and the extension built? Error: {e}")

    # Test the extension's behavior
    test_str = "abc" # a=97, b=98, c=99 -> sum=294
    result = _legacy_wrapper.process(test_str)
    assert result == 294, f"Expected _legacy_wrapper.process('abc') to return 294, got {result}"

def test_results_txt_correctness():
    assert os.path.isfile(RESULTS_FILE), f"{RESULTS_FILE} does not exist. Did you run your script and write the output?"

    # Compute expected results dynamically from stream.log to follow the principled testing rule
    assert os.path.isfile(STREAM_LOG), f"{STREAM_LOG} is missing."

    expected_results = []
    ip_counts = {}

    with open(STREAM_LOG, "r") as f:
        current_ip = None
        current_payload = []
        for line in f:
            line = line.strip()
            if line.startswith("START "):
                current_ip = line.split(" ", 1)[1]
                current_payload = []
            elif line.startswith("PAYLOAD:"):
                if current_ip is not None:
                    current_payload.append(line[8:])
            elif line == "END":
                if current_ip is not None:
                    count = ip_counts.get(current_ip, 0)
                    if count < 2:
                        ip_counts[current_ip] = count + 1
                        concat_str = "".join(current_payload)
                        # Compute sum of ascii values
                        ascii_sum = sum(ord(c) for c in concat_str)
                        expected_results.append(str(ascii_sum))
                    current_ip = None

    with open(RESULTS_FILE, "r") as f:
        actual_results = [line.strip() for line in f if line.strip()]

    assert actual_results == expected_results, f"Results in {RESULTS_FILE} do not match the expected values. Expected: {expected_results}, Got: {actual_results}"