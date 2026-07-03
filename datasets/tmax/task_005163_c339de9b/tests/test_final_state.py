# test_final_state.py

import os
import pytest
from collections import defaultdict

def test_c_source_exists():
    """Test that the C source code was created."""
    assert os.path.isfile('/home/user/project_graph.c'), "The C source file /home/user/project_graph.c is missing."

def test_c_executable_exists():
    """Test that the C program was compiled."""
    assert os.path.isfile('/home/user/project_graph'), "The compiled executable /home/user/project_graph is missing."
    assert os.access('/home/user/project_graph', os.X_OK), "The file /home/user/project_graph is not executable."

def test_coauthors_csv_correctness():
    """Test that the output coauthors.csv matches the expected graph projection."""
    input_path = '/home/user/wrote.csv'
    output_path = '/home/user/coauthors.csv'

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Generate ground truth from input file
    paper_to_authors = defaultdict(list)
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                a, p = parts
                paper_to_authors[p].append(a)

    coauthors = defaultdict(int)
    for p, auths in paper_to_authors.items():
        # Ensure unique authors per paper just in case, though the setup makes them unique
        auths = list(set(auths))
        for i in range(len(auths)):
            for j in range(i + 1, len(auths)):
                a1, a2 = auths[i], auths[j]
                if a1 > a2:
                    a1, a2 = a2, a1
                coauthors[(a1, a2)] += 1

    expected_lines = []
    for (a1, a2) in sorted(coauthors.keys()):
        expected_lines.append(f"{a1},{a2},{coauthors[(a1, a2)]}")

    expected_output = "\n".join(expected_lines)

    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, "The contents of /home/user/coauthors.csv do not match the expected graph projection."