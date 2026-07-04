# test_final_state.py

import os
import stat

def test_c_source_code_exists():
    file_path = "/home/user/analyze_backup.c"
    assert os.path.exists(file_path), f"C source file {file_path} is missing."

def test_compiled_executable_exists_and_executable():
    file_path = "/home/user/analyze_backup"
    assert os.path.exists(file_path), f"Compiled executable {file_path} is missing."
    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{file_path} is not executable."

def test_critical_node_output():
    file_path = "/home/user/critical_node.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "1,3", f"Expected '1,3' in {file_path}, but got '{content}'."

def test_cypher_query_validation():
    file_path = "/home/user/validation_query.cypher"
    assert os.path.exists(file_path), f"Cypher query file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().upper()

    # Check for essential Cypher constructs
    assert "MATCH" in content, "Cypher query is missing MATCH clause."
    assert "ORDER BY" in content, "Cypher query is missing ORDER BY clause."
    assert "DESC" in content, "Cypher query is missing DESC ordering."
    assert "LIMIT 1" in content, "Cypher query is missing LIMIT 1."
    assert "COUNT" in content, "Cypher query is missing COUNT function."