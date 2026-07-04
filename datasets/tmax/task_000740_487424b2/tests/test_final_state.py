# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

SCRIPT_PATH = "/home/user/deploy_mock_lib.sh"
DEPS_PATH = "/home/user/deps.json"
LOG_PATH = "/home/user/pipeline.log"

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """Ensure the script exists, is executable, and run it before tests."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

def test_pipeline_log_content():
    """Check that the pipeline.log contains exactly 'MOCK_BUILT'."""
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} was not created."
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
    assert content == "MOCK_BUILT", f"Expected log content 'MOCK_BUILT', got '{content}'"

def test_shared_library_exists_and_elf():
    """Verify the shared library is generated and is a valid ELF file."""
    with open(DEPS_PATH, "r") as f:
        deps = json.load(f)
    lib_name = deps.get("lib_name", "libwebsec")

    so_path = f"/home/user/build/{lib_name}.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not created."

    with open(so_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {so_path} is not a valid ELF file."

def test_shared_library_exports_symbol():
    """Verify the shared library exports the expected symbol."""
    with open(DEPS_PATH, "r") as f:
        deps = json.load(f)
    lib_name = deps.get("lib_name", "libwebsec")
    symbol = deps.get("symbol", "websec_verify_token")

    so_path = f"/home/user/build/{lib_name}.so"

    # Use nm to check exported symbols
    result = subprocess.run(["nm", "-D", so_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run nm on {so_path}"

    # Look for the symbol in the output
    exported = False
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "T" and parts[2] == symbol:
            exported = True
            break

    assert exported, f"Symbol '{symbol}' is not exported as a global text symbol (T) in {so_path}."