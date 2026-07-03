# test_final_state.py
import os
import subprocess

def test_script_execution_and_output():
    script_path = '/home/user/ticket_8492/process_logs.py'
    output_path = '/home/user/ticket_8492/output.txt'

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Remove output.txt if it exists to ensure we are testing the script's actual output
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the script with a timeout to detect deadlocks
    try:
        result = subprocess.run(
            ['python3', script_path],
            timeout=10,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        assert False, "The script timed out, which indicates the threading deadlock has not been fully resolved."

    assert result.returncode == 0, f"The script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the script."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "100", f"Expected the final sum in {output_path} to be '100', but got '{content}'."