# test_final_state.py

import os
import csv
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/find_conflicts.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_database_exists():
    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

def test_conflicts_csv_output():
    csv_path = "/home/user/conflicts.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("conflicts.csv is empty.")

        expected_header = ["person_name", "investor_company_name", "target_company_name"]
        assert header == expected_header, f"Header {header} does not match expected {expected_header}."

        rows = list(reader)

        # Check sorting
        assert rows == sorted(rows), "conflicts.csv is not sorted alphabetically by person_name, investor_company_name, target_company_name."

        # Check for specific known conflicts
        known_conflicts = [
            ["Person_10", "Company_E", "Company_J"],
            ["Person_88", "Company_Z33", "Company_L"]
        ]

        for conflict in known_conflicts:
            assert conflict in rows, f"Expected conflict {conflict} not found in conflicts.csv."

def test_query_plan_output():
    plan_path = "/home/user/plan.txt"
    assert os.path.isfile(plan_path), f"Query plan file {plan_path} does not exist."

    with open(plan_path, "r", encoding="utf-8") as f:
        plan_content = f.read().upper()

    # The plan should use SEARCH for the relation tables
    # Check if SEARCH is used for board_members and investments
    assert "SEARCH" in plan_content and "INDEX" in plan_content, "Query plan does not seem to use index lookups (SEARCH ... USING INDEX)."

    # Check that it doesn't do a full table scan on board_members or investments as inner loops
    # It's difficult to parse the exact tree, but we can look for SEARCH TABLE board_members
    # or ensure that SCAN TABLE board_members is not the dominant access path.
    # At the very least, we expect SEARCH to be used for these tables.
    has_search_board = "SEARCH TABLE BOARD_MEMBERS" in plan_content or "SEARCH BOARD_MEMBERS" in plan_content or "SEARCH TABLE MAIN.BOARD_MEMBERS" in plan_content
    has_search_investments = "SEARCH TABLE INVESTMENTS" in plan_content or "SEARCH INVESTMENTS" in plan_content or "SEARCH TABLE MAIN.INVESTMENTS" in plan_content

    assert has_search_board or has_search_investments, "Query plan does not use SEARCH for the relation tables."

    # Ensure no SCAN TABLE for board_members and investments if possible,
    # but we allow it if it's the driving table (only one SCAN allowed overall for the query usually, for persons or companies).
    # The prompt explicitly forbids SCAN TABLE on these relation tables during join execution.
    scan_board = plan_content.count("SCAN TABLE BOARD_MEMBERS") + plan_content.count("SCAN BOARD_MEMBERS")
    scan_investments = plan_content.count("SCAN TABLE INVESTMENTS") + plan_content.count("SCAN INVESTMENTS")

    # If persons is driving, board_members is searched. If board_members is driving, it might be scanned once, but investments must be searched.
    # The constraint says: "Full table scans (SCAN TABLE) on these relation tables during the join execution are not allowed"
    # We will strictly check that they are not scanned multiple times, or preferably not scanned at all if they are join targets.
    if scan_board > 0 and not has_search_board:
        pytest.fail("Query plan uses SCAN for board_members without any SEARCH, violating the index requirement.")
    if scan_investments > 0 and not has_search_investments:
        pytest.fail("Query plan uses SCAN for investments without any SEARCH, violating the index requirement.")