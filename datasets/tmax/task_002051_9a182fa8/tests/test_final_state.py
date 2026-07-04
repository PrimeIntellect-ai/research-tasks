# test_final_state.py

import os
import re

def test_migrate_patched():
    path = "/home/user/migrate.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "statistics.mean" in content, f"{path} was not patched correctly (missing statistics.mean)."
    assert "sum(v1_data" not in content, f"{path} still contains the bug."

def test_test_migration_py_created():
    path = "/home/user/test_migration.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "test_migration_invariants" in content, "Test function 'test_migration_invariants' not found."
    assert "@given" in content, "@given decorator from hypothesis not found in the test file."
    assert "isclose" in content, "math.isclose not found in the test file."

def test_test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you redirect the pytest output?"
    with open(path, "r") as f:
        content = f.read()

    # Pytest output usually ends with something like "1 passed in 0.12s"
    assert re.search(r"\b1 passed\b", content) is not None, "Log file does not indicate that 1 test passed."