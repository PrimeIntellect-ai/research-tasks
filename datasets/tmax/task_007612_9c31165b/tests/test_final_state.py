# test_final_state.py

import os

def test_output_csv_exists_and_correct():
    output_path = "/home/user/output.csv"
    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

    expected_content = (
        "user_id,login_count,purchase_count\n"
        "102,2,1\n"
        "104,2,1\n"
        "201,2,2\n"
        "202,2,2\n"
    )

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read().replace("\r\n", "\n").strip() + "\n"

    assert actual_content == expected_content, (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_c_program_exists():
    source_path = "/home/user/process.c"
    assert os.path.isfile(source_path), f"C source file missing at {source_path}"

def test_executable_exists():
    exec_path = "/home/user/process"
    assert os.path.isfile(exec_path), f"Compiled executable missing at {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File at {exec_path} is not executable"

def test_database_unmodified():
    db_path = "/home/user/data.db"
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    # The database was set to 444 (read-only) in setup.
    # We can verify it's still read-only or just that the file exists.
    # A simple check to ensure it hasn't been deleted or replaced.
    st = os.stat(db_path)
    assert oct(st.st_mode)[-3:] in ['444', '400', '644'], "Database permissions suggest it might have been modified or recreated incorrectly"