# test_final_state.py
import os
import sqlite3

def test_result_txt_exists_and_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "1000", f"Incorrect sum in {path}. Expected '1000', got '{content}'."

def test_c_source_file_exists():
    path = "/home/user/process_datasets.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_sqlite_db_exists_and_schema():
    db_path = "/home/user/research.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='datasets';")
    table = cursor.fetchone()
    assert table is not None, "Table 'datasets' does not exist in the database."

    # Check if index exists on datasets table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='datasets';")
    indexes = cursor.fetchall()
    assert len(indexes) >= 1, "No index created on 'datasets' table."

    # Check if data was inserted
    cursor.execute("SELECT count(*) FROM datasets;")
    count = cursor.fetchone()[0]
    assert count > 0, "No data inserted into 'datasets' table."

    # Check if parent_id index is on the parent_id column
    # We can check the index info
    index_on_parent_id = False
    for idx in indexes:
        idx_name = idx[0]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        cols = cursor.fetchall()
        for col in cols:
            if col[2] == 'parent_id':
                index_on_parent_id = True
                break
        if index_on_parent_id:
            break

    assert index_on_parent_id, "No index found specifically on the 'parent_id' column."

    conn.close()