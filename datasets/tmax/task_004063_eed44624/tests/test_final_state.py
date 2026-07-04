# test_final_state.py
import os
import stat
import subprocess
import tempfile
import pytest

def test_test_status_file():
    """Verify that the test status file exists and contains the success message."""
    status_file = "/home/user/test_status.txt"
    assert os.path.isfile(status_file), f"The file {status_file} does not exist. Did you run your test script?"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "REPRODUCIBLE AND ACCURATE", f"Expected 'REPRODUCIBLE AND ACCURATE' in {status_file}, but got '{content}'"

def test_scripts_exist_and_executable():
    """Verify that both required scripts exist and are executable."""
    pipeline_script = "/home/user/run_pipeline.sh"
    test_script = "/home/user/test_accuracy.sh"

    for script in [pipeline_script, test_script]:
        assert os.path.isfile(script), f"The script {script} does not exist."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"The script {script} is not executable."

def test_pipeline_no_forbidden_tools():
    """Ensure the pipeline script does not use forbidden languages."""
    pipeline_script = "/home/user/run_pipeline.sh"
    with open(pipeline_script, "r") as f:
        content = f.read().lower()

    forbidden = ["python", "perl", "rscript"]
    for tool in forbidden:
        assert tool not in content, f"Forbidden tool '{tool}' found in {pipeline_script}. You must use standard shell tools."

def test_pipeline_logic_on_hidden_data():
    """Test the pipeline script on a new, hidden dataset to ensure it calculates correctly and doesn't hardcode output."""
    pipeline_script = "/home/user/run_pipeline.sh"

    with tempfile.TemporaryDirectory() as tmpdir:
        tx_file = os.path.join(tmpdir, "tx_hidden.csv")
        fx_file = os.path.join(tmpdir, "fx_hidden.csv")
        out_file = os.path.join(tmpdir, "out_hidden.csv")

        # Create hidden transaction data
        with open(tx_file, "w") as f:
            f.write("tx_id,date,currency,amount\n")
            f.write("1,2023-11-01,CAD,100.00\n")
            f.write("2,2023-11-01,AUD,50.00\n")
            f.write("3,2023-11-02,CAD,200.50\n")

        # Create hidden exchange rate data
        with open(fx_file, "w") as f:
            f.write("date,currency,rate\n")
            f.write("2023-11-01,CAD,0.75\n")
            f.write("2023-11-01,AUD,0.65\n")
            f.write("2023-11-02,CAD,0.74\n")

        # Expected Math:
        # 2023-11-01: (100.00 * 0.75) + (50.00 * 0.65) = 75.00 + 32.50 = 107.50
        # 2023-11-02: (200.50 * 0.74) = 148.37

        result = subprocess.run([pipeline_script, tx_file, fx_file, out_file], capture_output=True, text=True)
        assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStderr: {result.stderr}"

        assert os.path.isfile(out_file), f"Pipeline script did not create the expected output file at {out_file}."

        with open(out_file, "r") as f:
            out_lines = [line.strip() for line in f if line.strip()]

        assert len(out_lines) == 3, f"Output should have exactly 3 lines (header + 2 data rows), found {len(out_lines)}."
        assert out_lines[0] == "date,total_usd", f"Output header is incorrect. Expected 'date,total_usd', got '{out_lines[0]}'."
        assert out_lines[1] == "2023-11-01,107.50", f"Data mismatch for 2023-11-01. Expected '2023-11-01,107.50', got '{out_lines[1]}'."
        assert out_lines[2] == "2023-11-02,148.37", f"Data mismatch for 2023-11-02. Expected '2023-11-02,148.37', got '{out_lines[2]}'."