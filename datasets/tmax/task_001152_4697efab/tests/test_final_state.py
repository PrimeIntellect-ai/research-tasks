# test_final_state.py

import os
import csv
import subprocess
import pytest

def get_gc_content(sequence):
    seq = sequence.strip()
    if not seq:
        return 0.0
    gc_count = sum(1 for c in seq.upper() if c in ('G', 'C'))
    return gc_count / len(seq)

def solve_euler(r):
    P = 10.0
    for _ in range(100):
        P += 0.1 * r * P * (1.0 - P / 1000.0)
    return f"{P:.2f}"

def test_workspace_and_files():
    assert os.path.isdir("/home/user/bio_sim"), "Workspace directory /home/user/bio_sim does not exist."
    assert os.path.isfile("/home/user/bio_sim/go.mod"), "go.mod does not exist in /home/user/bio_sim."
    assert os.path.isfile("/home/user/bio_sim/main.go"), "main.go does not exist in /home/user/bio_sim."
    assert os.path.isfile("/home/user/bio_sim/main_test.go"), "main_test.go does not exist in /home/user/bio_sim."

def test_go_test_passes():
    result = subprocess.run(
        ["go", "test"],
        cwd="/home/user/bio_sim",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed in /home/user/bio_sim.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_go_run_generates_correct_csv():
    # Run the program to ensure it generates the CSV properly
    result = subprocess.run(
        ["go", "run", "main.go"],
        cwd="/home/user/bio_sim",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go run main.go' failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    csv_path = "/home/user/results.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} was not generated."

    # Compute expected results
    fasta_path = "/home/user/input.fasta"
    assert os.path.isfile(fasta_path), f"Input FASTA {fasta_path} is missing."

    expected_results = {}
    with open(fasta_path, "r") as f:
        current_id = None
        current_seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    r = get_gc_content("".join(current_seq))
                    expected_results[current_id] = solve_euler(r)
                current_id = line[1:].strip()
                current_seq = []
            else:
                current_seq.append(line)
        if current_id is not None:
            r = get_gc_content("".join(current_seq))
            expected_results[current_id] = solve_euler(r)

    # Read actual results
    actual_results = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["StrainID", "FinalPopulation"], f"CSV header is incorrect. Expected ['StrainID', 'FinalPopulation'], got {header}"
        for row in reader:
            if len(row) != 2:
                continue
            actual_results[row[0].strip()] = row[1].strip()

    # Compare
    for strain_id, expected_pop in expected_results.items():
        assert strain_id in actual_results, f"StrainID {strain_id} missing from {csv_path}."
        actual_pop = actual_results[strain_id]

        # Allow small floating point differences in formatting, but exact string match is preferred since the prompt asks for exactly 2 decimal places.
        assert actual_pop == expected_pop, f"For {strain_id}, expected FinalPopulation {expected_pop}, but got {actual_pop}."