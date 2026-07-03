# test_final_state.py

import os
import subprocess
import time

def test_failing_input_file():
    path = "/home/user/failing_input.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "HALT", f"Expected failing input to be 'HALT', but got '{content}'."

def test_missing_file_txt():
    path = "/home/user/missing_file.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "/tmp/worker.sock", f"Expected missing file path to be '/tmp/worker.sock', but got '{content}'."

def test_process_data_sh_fixed_code():
    path = "/home/user/process_data.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "sleep 0.1" not in content, "The script still contains 'sleep 0.1'."
    assert "while [" not in content or "worker.sock" not in content[content.find("while ["):content.find("do", content.find("while ["))], \
        "The script appears to still have a while loop waiting for the socket."

def test_process_data_sh_execution():
    script_path = "/home/user/process_data.sh"
    input_path = "/home/user/words.txt"

    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    start_time = time.time()
    try:
        result = subprocess.run(
            [script_path, input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2.0
        )
    except subprocess.TimeoutExpired:
        assert False, "The script timed out, indicating it is still hanging."

    duration = time.time() - start_time
    assert duration < 1.0, f"Script took too long to execute ({duration:.2f}s), might still be hanging."

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert "Error: worker missing" in result.stdout, "The script output did not contain the expected error message 'Error: worker missing'."