# test_final_state.py
import os
import subprocess
import time
import stat

def test_script_exists_and_executable():
    script_path = "/home/user/plan_restore.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_script_execution_and_output():
    script_path = "/home/user/plan_restore.sh"

    start_time = time.time()
    try:
        result = subprocess.run(
            ["bash", script_path, "NodeF"],
            capture_output=True,
            text=True,
            timeout=5.0
        )
        elapsed = time.time() - start_time
    except subprocess.TimeoutExpired:
        assert False, "The script execution timed out (exceeded 5.0 seconds)."

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr.strip()}"

    output = result.stdout.strip()

    assert output == "65", f"Expected output '65', but got '{output}'."
    assert elapsed < 1.0, f"Script execution took {elapsed:.3f} seconds, which exceeds the 1.0 second limit. Did you forget to index the database?"