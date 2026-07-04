# test_final_state.py
import os
import subprocess

def test_extracted_tx_file():
    path = "/home/user/extracted_tx.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you extract the transaction ID?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "TXID-84729-OMEGA", f"Extracted TXID is incorrect. Found: '{content}'"

def test_cargo_test_passes():
    project_dir = "/home/user/risk_engine"
    assert os.path.exists(project_dir), f"Project directory {project_dir} is missing."

    # Run cargo test to verify compilation and the precision fix (which has a test in main.rs)
    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed. Compilation or precision error not resolved.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_final_score_file():
    path = "/home/user/final_score.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you run the program and save the output?"
    with open(path, "r") as f:
        content = f.read().strip()

    # The expected f64 precision result calculated in the Rust code
    expected_score = "37783.43433288728"

    # Check if the score matches the expected output
    try:
        score_val = float(content)
        expected_val = float(expected_score)
        assert abs(score_val - expected_val) < 1e-5, f"Final score in {path} is incorrect. Expected approx {expected_score}, got {content}"
    except ValueError:
        assert False, f"Content of {path} is not a valid float: '{content}'"