# test_final_state.py
import os

def test_csv_files_exist():
    """Check if the dataset CSV files exist and contain the correct headers/content."""
    users_csv = "/home/user/data/users.csv"
    transactions_csv = "/home/user/data/transactions.csv"

    assert os.path.isfile(users_csv), f"Missing file: {users_csv}"
    assert os.path.isfile(transactions_csv), f"Missing file: {transactions_csv}"

    with open(users_csv, "r") as f:
        content = f.read().strip()
        assert "user_id,name" in content, "users.csv does not contain the correct header."
        assert "1,Alice" in content, "users.csv does not contain Alice."

    with open(transactions_csv, "r") as f:
        content = f.read().strip()
        assert "tx_id,sender_id,receiver_id,amount" in content, "transactions.csv does not contain the correct header."
        assert "101,1,2,50.0" in content, "transactions.csv missing expected data."

def test_c_program_exists():
    """Check if the C source code and compiled binary exist."""
    c_source = "/home/user/analyze_graph.c"
    binary = "/home/user/analyze_graph"

    assert os.path.isfile(c_source), f"Missing C source file: {c_source}"
    assert os.path.isfile(binary), f"Missing compiled binary: {binary}"
    assert os.access(binary, os.X_OK), f"Compiled binary {binary} is not executable."

def test_centrality_report():
    """Check if the centrality report exists and contains the correct sorted output."""
    report_file = "/home/user/centrality_report.txt"
    assert os.path.isfile(report_file), f"Missing output report: {report_file}"

    expected_output = [
        "2,Bob,255.0",
        "4,Diana,160.0",
        "5,Eve,125.0",
        "3,Charlie,110.0",
        "1,Alice,80.0"
    ]

    with open(report_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_output, (
        f"Report content does not match expected output.\n"
        f"Expected: {expected_output}\n"
        f"Got: {lines}"
    )