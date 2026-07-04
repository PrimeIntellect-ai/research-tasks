# test_final_state.py

import os
import stat
import subprocess

def test_bug_line():
    bug_line_path = "/home/user/bug_line.txt"
    assert os.path.exists(bug_line_path), f"File {bug_line_path} does not exist."
    with open(bug_line_path, 'r') as f:
        content = f.read().strip()
    assert content == "432", f"Expected bug_line.txt to contain '432', got '{content}'."

def test_total_bytes():
    total_bytes_path = "/home/user/total_bytes.txt"
    assert os.path.exists(total_bytes_path), f"File {total_bytes_path} does not exist."
    with open(total_bytes_path, 'r') as f:
        content = f.read().strip()
    assert content == "99850", f"Expected total_bytes.txt to contain '99850', got '{content}'."

def test_fixed_script():
    fixed_script_path = "/home/user/parse_pcap_fixed.sh"
    log_path = "/home/user/traffic.log"

    assert os.path.exists(fixed_script_path), f"File {fixed_script_path} does not exist."

    st = os.stat(fixed_script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {fixed_script_path} is not executable."

    # Run the script with a timeout to catch infinite loops
    try:
        result = subprocess.run(
            [fixed_script_path, log_path],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"The script {fixed_script_path} timed out, indicating an infinite loop.")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    expected_output = "Total: 99850"
    assert expected_output in output, f"Expected output to contain '{expected_output}', got '{output}'."

    # Check that there are no syntax errors or mathematical evaluation errors in stderr
    assert result.stderr.strip() == "", f"Expected no stderr output, got '{result.stderr}'"