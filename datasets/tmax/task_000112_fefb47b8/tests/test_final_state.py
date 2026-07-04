# test_final_state.py

import os
import glob

WORKSPACE_DIR = "/home/user/workspace"
FLAG_PATH = os.path.join(WORKSPACE_DIR, "flag.txt")
ANALYZE_SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "analyze.py")

def test_flag_file_exists_and_correct():
    assert os.path.isfile(FLAG_PATH), f"Flag file not found at {FLAG_PATH}"

    with open(FLAG_PATH, "r") as f:
        content = f.read().strip()

    # The expected calculation from the pcap payload [4815, 162342, 31415, 9265, 3589]
    # Total = 4815*1 + 162342*2 + 31415*3 + 9265*4 + 3589*5 = 478749
    # 478749 % 9973 = 45
    expected_value = "45"

    assert content == expected_value, f"Flag content is incorrect. Expected '{expected_value}', got '{content}'."

def test_analyze_script_exists():
    assert os.path.isfile(ANALYZE_SCRIPT_PATH), f"Analysis script not found at {ANALYZE_SCRIPT_PATH}"

def test_extension_compiled():
    # Check if a compiled shared object exists for the decoder module
    so_files = glob.glob(os.path.join(WORKSPACE_DIR, "decoder*.so"))
    assert len(so_files) > 0, "Compiled decoder extension (.so file) not found in the workspace. Build may have failed or was not run in-place."