# test_final_state.py
import os
import subprocess

def test_trace_txt_exists_and_correct():
    """Verify that trace.txt exists and contains the correct trace value."""
    trace_file = "/home/user/trace.txt"
    assert os.path.exists(trace_file), f"File {trace_file} does not exist."

    with open(trace_file, "r") as f:
        content = f.read().strip()

    assert content == "126.9821", f"Expected trace value '126.9821', but got '{content}'."

def test_fasta_file_exists():
    """Verify that sequences.fasta exists with correct content."""
    fasta_file = "/home/user/sequences.fasta"
    assert os.path.exists(fasta_file), f"File {fasta_file} does not exist."

    with open(fasta_file, "r") as f:
        content = f.read()

    expected_sequences = ["AAAAA", "ACGTG", "AAAAAC", "TTTTT"]
    for seq in expected_sequences:
        assert seq in content, f"Expected sequence '{seq}' not found in {fasta_file}."

def test_go_app_files_exist():
    """Verify that main.go and main_test.go exist."""
    main_go = "/home/user/kmer_app/main.go"
    main_test_go = "/home/user/kmer_app/main_test.go"
    go_mod = "/home/user/kmer_app/go.mod"

    assert os.path.exists(main_go), f"File {main_go} does not exist."
    assert os.path.exists(main_test_go), f"File {main_test_go} does not exist."
    assert os.path.exists(go_mod), f"File {go_mod} does not exist."

def test_go_test_file_content():
    """Verify that main_test.go contains tests for 'ACGTG' and 'CG'."""
    main_test_go = "/home/user/kmer_app/main_test.go"

    with open(main_test_go, "r") as f:
        content = f.read()

    assert "ACGTG" in content, "main_test.go does not contain the test sequence 'ACGTG'."
    assert "CG" in content, "main_test.go does not check for the 'CG' 2-mer."

def test_go_tests_pass():
    """Verify that go test passes in the kmer_app directory."""
    app_dir = "/home/user/kmer_app"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."

    result = subprocess.run(
        ["go", "test"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"'go test' failed in {app_dir}:\n{result.stderr}\n{result.stdout}"