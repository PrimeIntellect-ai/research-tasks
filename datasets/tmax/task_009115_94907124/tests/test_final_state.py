# test_final_state.py
import os
import sys
import sqlite3
import ast
import subprocess
import pytest

def test_task1_extension_installed():
    # Remove local paths to ensure it's installed globally
    original_path = sys.path.copy()
    try:
        sys.path = [p for p in sys.path if not p.startswith('/home/user/app/ext')]
        try:
            import sec_ext
        except ImportError as e:
            pytest.fail(f"Failed to import sec_ext: {e}. Ensure it is installed globally and linked correctly.")
    finally:
        sys.path = original_path

    # Check setup.py for rpath
    setup_py_path = "/home/user/app/ext/setup.py"
    assert os.path.isfile(setup_py_path), "setup.py is missing."
    with open(setup_py_path, 'r') as f:
        content = f.read()
        assert "runtime_library_dirs" in content or "-Wl,-rpath" in content, "setup.py does not contain rpath configuration."

def test_task2_database_migration():
    db_path = "/home/user/app/db/chat.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(messages)")
    columns = [row[1] for row in cursor.fetchall()]
    assert "msg_hash" in columns, "Column 'msg_hash' was not added to 'messages' table."

    cursor.execute("SELECT content, msg_hash FROM messages")
    rows = cursor.fetchall()

    import sec_ext
    for content, msg_hash in rows:
        expected_hash = sec_ext.compute_hash(content)
        assert msg_hash == expected_hash, f"Hash mismatch for content '{content}'. Expected {expected_hash}, got {msg_hash}."

    conn.close()

def test_task3_test_ws_script():
    test_script_path = "/home/user/app/test_ws.py"
    assert os.path.isfile(test_script_path), f"{test_script_path} is missing."

    with open(test_script_path, 'r') as f:
        content = f.read()

    assert "import pytest" in content, "test_ws.py must import pytest."
    assert "hypothesis" in content, "test_ws.py must use hypothesis."
    assert "@given" in content, "test_ws.py must use @given from hypothesis."
    assert "st.integers" in content, "test_ws.py must use st.integers()."
    assert "st.text" in content, "test_ws.py must use st.text()."
    assert "ws://localhost:8080" in content, "test_ws.py must connect to ws://localhost:8080."

    # Verify it can be collected by pytest
    result = subprocess.run(
        ["pytest", test_script_path, "--collect-only"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed to collect tests from {test_script_path}:\n{result.stderr}\n{result.stdout}"