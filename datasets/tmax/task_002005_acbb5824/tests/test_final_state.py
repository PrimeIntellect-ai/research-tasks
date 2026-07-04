# test_final_state.py
import os
import sqlite3
import pytest

def test_top_nodes_csv():
    csv_path = '/home/user/top_nodes.csv'
    assert os.path.isfile(csv_path), f"{csv_path} does not exist. Did you run the Rust program?"

    expected_content = (
        "type,name,total_weight\n"
        "Database,TransactionDB,25.0\n"
        "Queue,JobQueue,20.0\n"
        "Service,AuthService,16.0\n"
    )

    with open(csv_path, 'r') as f:
        content = f.read()

    # Normalize line endings and strip trailing whitespace
    content_lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines() if line.strip()]

    assert content_lines == expected_lines, f"Content of {csv_path} does not match expected output."

def test_database_integrity():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"{db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()

    assert result is not None, "Failed to run integrity check."
    assert result[0].lower() == 'ok', "Database integrity check failed. Did you run REINDEX on idx_edges_target?"

    conn.close()

def test_rust_project_exists():
    main_rs_path = '/home/user/graph_analyzer/src/main.rs'
    cargo_toml_path = '/home/user/graph_analyzer/Cargo.toml'

    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist."
    assert os.path.isfile(cargo_toml_path), f"{cargo_toml_path} does not exist."