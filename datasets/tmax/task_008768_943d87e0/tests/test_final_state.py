# test_final_state.py

import os
import pytest

def test_top_type_file_exists_and_correct():
    """Check if top_type.txt exists and contains the correct entity type."""
    file_path = '/home/user/top_type.txt'
    assert os.path.exists(file_path), f"Output file missing at {file_path}"
    assert os.path.isfile(file_path), f"{file_path} is not a file"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "Metabolite", f"Expected 'Metabolite', but found '{content}'"

def test_analyze_script_exists():
    """Check if the analyze.py script was created."""
    script_path = '/home/user/analyze.py'
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_analyze_script_bypasses_index():
    """Check if the script contains logic to bypass the index."""
    script_path = '/home/user/analyze.py'
    if not os.path.exists(script_path):
        pytest.fail("analyze.py script is missing, cannot check for index bypass.")

    with open(script_path, 'r') as f:
        content = f.read().lower()

    # Check for common SQLite index bypass methods
    bypassed = "not indexed" in content or "indexed by" in content or "+src" in content or "+ src" in content
    assert bypassed, "The script does not appear to explicitly bypass the index (e.g., using 'NOT INDEXED')."