# test_final_state.py
import os
import subprocess

def test_run_e2e_script_exists_and_executable():
    script_path = "/home/user/run_e2e.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_file_content():
    report_path = "/home/user/test_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "PASS", f"Expected report content to be 'PASS', but got '{content}'."

def test_servers_are_cleaned_up():
    try:
        # Check for legacy_api.py
        legacy_check = subprocess.run(["pgrep", "-f", "legacy_api.py"], capture_output=True, text=True)
        assert legacy_check.returncode != 0, "legacy_api.py process is still running; it was not cleaned up."

        # Check for new_api.py
        new_check = subprocess.run(["pgrep", "-f", "new_api.py"], capture_output=True, text=True)
        assert new_check.returncode != 0, "new_api.py process is still running; it was not cleaned up."
    except FileNotFoundError:
        # If pgrep is not found, we can try using ps
        ps_check = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        assert "legacy_api.py" not in ps_check.stdout or "grep" in ps_check.stdout, "legacy_api.py process is still running."
        assert "new_api.py" not in ps_check.stdout or "grep" in ps_check.stdout, "new_api.py process is still running."