# test_final_state.py

import os
import pytest

def test_violations_csv_exists_and_correct():
    """
    Verify that the user has successfully created the violations.csv file
    and that its contents exactly match the expected compliance violation pattern.
    """
    csv_file_path = "/home/user/violations.csv"

    # Check if the output file exists
    assert os.path.exists(csv_file_path), f"Expected output file {csv_file_path} is missing."
    assert os.path.isfile(csv_file_path), f"{csv_file_path} is not a file."

    # Read the contents
    with open(csv_file_path, "r") as f:
        content = f.read().strip()

    expected_content = "FraudX,FraudY,FraudZ\nShellA,ShellB,ShellC"

    # Compare ignoring trailing newlines
    assert content == expected_content, (
        f"Content of {csv_file_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )

def test_corporate_graph_ttl_unmodified():
    """
    Verify that the original corporate_graph.ttl file is still intact.
    """
    ttl_file_path = "/home/user/corporate_graph.ttl"

    assert os.path.exists(ttl_file_path), f"Original file {ttl_file_path} is missing."

    expected_content = """@prefix ex: <http://example.org/audit/> .

ex:ShellA ex:owns ex:ShellB .
ex:ShellB ex:owns ex:ShellC .
ex:ShellC ex:transactsWith ex:ShellA .

ex:LegitA ex:owns ex:LegitB .
ex:LegitB ex:owns ex:LegitC .
ex:LegitC ex:transactsWith ex:LegitD .

ex:FraudX ex:owns ex:FraudY .
ex:FraudY ex:owns ex:FraudZ .
ex:FraudZ ex:transactsWith ex:FraudX .

ex:Loop1 ex:transactsWith ex:Loop2 .
ex:Loop2 ex:transactsWith ex:Loop3 .
ex:Loop3 ex:transactsWith ex:Loop1 ."""

    with open(ttl_file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content.strip(), f"Original file {ttl_file_path} was modified."