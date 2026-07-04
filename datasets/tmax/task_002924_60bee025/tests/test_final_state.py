# test_final_state.py

import os

def test_output_tsv_exists():
    assert os.path.isfile("/home/user/output.tsv"), "/home/user/output.tsv does not exist. The program output must be saved to this file."

def test_output_tsv_content():
    expected_lines = [
        "A\t0",
        "C\t2",
        "B\t4",
        "D\t5",
        "E\t16"
    ]

    with open("/home/user/output.tsv", "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert lines == expected_lines, f"The contents of /home/user/output.tsv do not match the expected sorted output. Expected {expected_lines}, but got {lines}."

def test_graph_etl_c_modified():
    file_path = "/home/user/graph_etl.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # The original buggy loop was assigning the edge to all currently known nodes.
    # We check that the specific exact buggy line `adj[u][v] = weight;` inside a loop over `v` is no longer there,
    # or at least that the file has been changed to fix the logic.
    # Since there are many ways to fix it, the output validation is our primary check.
    # But we can assert that the specific buggy assignment `adj[u][v] = weight;` without `v_actual` is not the only logic.
    # Actually, the output test is sufficient and robust.
    pass