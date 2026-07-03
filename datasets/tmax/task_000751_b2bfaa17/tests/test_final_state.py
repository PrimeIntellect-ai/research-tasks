# test_final_state.py
import os
import sqlite3
import stat

def test_run_pipeline_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

def test_closest_txt():
    output_path = '/home/user/closest.txt'
    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "73", f"Expected closest ID to be 73, but got '{content}'"

def test_sqlite_db():
    db_path = '/home/user/embeddings.db'
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'")
    assert cursor.fetchone() is not None, "Table 'embeddings' does not exist in the database"

    # Check schema
    cursor.execute("PRAGMA table_info(embeddings)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = ['id', 'a', 'e', 'i', 'o', 'u']
    for col in expected_columns:
        assert col in columns, f"Column '{col}' missing in 'embeddings' table"

    # Check specific row for ID 42
    cursor.execute("SELECT a, e, i, o, u FROM embeddings WHERE id=42")
    row_42 = cursor.fetchone()
    assert row_42 is not None, "Row for ID 42 missing in 'embeddings' table"
    assert row_42 == (7, 7, 6, 4, 3), f"Expected embedding for ID 42 to be (7, 7, 6, 4, 3), got {row_42}"

    # Check specific row for ID 73
    cursor.execute("SELECT a, e, i, o, u FROM embeddings WHERE id=73")
    row_73 = cursor.fetchone()
    assert row_73 is not None, "Row for ID 73 missing in 'embeddings' table"
    assert row_73 == (4, 4, 3, 4, 4), f"Expected embedding for ID 73 to be (4, 4, 3, 4, 4), got {row_73}"

    conn.close()

def test_rust_project_exists():
    cargo_toml_path = '/home/user/vowel_embedder/Cargo.toml'
    assert os.path.isfile(cargo_toml_path), f"Rust project missing Cargo.toml at {cargo_toml_path}"