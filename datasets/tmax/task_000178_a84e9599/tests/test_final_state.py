# test_final_state.py
import os
import sqlite3
import stat
import pytest

def test_db_schema():
    db_path = "/home/user/waf/waf.db"
    assert os.path.isfile(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(rules);")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()

    assert "id" in columns, "Column 'id' missing in 'rules' table."
    assert "pattern" in columns, "Column 'pattern' missing in 'rules' table."
    assert "action" in columns, "Column 'action' missing in 'rules' table. Did you apply v2_update.sql?"

def test_c_memory_safety():
    parser_c = "/home/user/waf/c_src/parser.c"
    assert os.path.isfile(parser_c), f"Missing {parser_c}"

    with open(parser_c, "r") as f:
        content = f.read()

    assert "malloc(16)" not in content, "The C source file still contains the hardcoded malloc(16)."
    assert "strlen" in content or "strdup" in content, "The C source file should dynamically allocate memory using strlen or strdup."

def test_go_circular_import_resolved():
    config_go = "/home/user/waf/go_src/config/config.go"
    assert os.path.isfile(config_go), f"Missing {config_go}"

    with open(config_go, "r") as f:
        content = f.read()

    assert '"waf/engine"' not in content, "The config.go file still contains the circular import to waf/engine."

def test_ci_script_exists_and_executable():
    script_path = "/home/user/run_ci.sh"
    assert os.path.isfile(script_path), f"Missing CI script: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "set -e" in content, "The script must contain 'set -e' to fail immediately on errors."

def test_build_artifacts_exist():
    lib_path = "/home/user/waf/libparser.so"
    bin_path = "/home/user/waf/waf_binary"

    assert os.path.isfile(lib_path), f"Shared library missing: {lib_path}"
    assert os.path.isfile(bin_path), f"Go binary missing: {bin_path}"

    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Go binary {bin_path} is not executable."

def test_test_report_output():
    report_path = "/home/user/waf/test_report.txt"
    assert os.path.isfile(report_path), f"Test report missing: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "Payload: DROP TABLE users;, Result: BLOCKED"
    assert expected in content, f"Test report does not contain the expected output. Found: {content}"