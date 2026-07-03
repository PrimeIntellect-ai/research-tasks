# test_final_state.py
import os

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_venv_and_csvkit_installed():
    csvcut_path = "/home/user/venv/bin/csvcut"
    assert os.path.isfile(csvcut_path), "csvkit does not appear to be installed in the virtual environment at /home/user/venv."

def test_master_log_csv():
    master_log_path = "/home/user/processed/master_log.csv"
    assert os.path.isfile(master_log_path), f"The file {master_log_path} does not exist."

    with open(master_log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 lines in {master_log_path}, but found {len(lines)}."

    header_count = sum(1 for line in lines if line == "IP,Date,Endpoint,Status")
    assert header_count == 1, f"Expected exactly one header row 'IP,Date,Endpoint,Status' in {master_log_path}, but found {header_count}."
    assert lines[0] == "IP,Date,Endpoint,Status", "The first line of master_log.csv must be the header."

def test_summary_md():
    summary_path = "/home/user/reports/summary.md"
    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "# Endpoint Summary\n"
        "- /api/auth: 3\n"
        "- /api/data: 3\n"
        "- /api/users: 3"
    )

    assert content == expected_content, f"The content of {summary_path} does not match the expected output."