# test_final_state.py
import os
import subprocess

APP_DIR = "/home/user/app"

def test_solution_file():
    solution_path = os.path.join(APP_DIR, "solution.txt")
    assert os.path.exists(solution_path), f"Solution file {solution_path} does not exist."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Solution file does not contain a valid float: {content}"

    assert val == 150.0, f"Expected solution to be 150.0, but got {val}"

def test_run_job_succeeds():
    runner_path = os.path.join(APP_DIR, "run_job.sh")
    assert os.path.exists(runner_path), f"Runner script {runner_path} is missing."

    result = subprocess.run(["bash", runner_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_job.sh failed with output: {result.stderr}\n{result.stdout}"

    output = result.stdout.strip()
    try:
        val = float(output)
    except ValueError:
        assert False, f"run_job.sh did not output a valid float: {output}"

    assert val == 150.0, f"Expected run_job.sh to output 150.0, but got {val}"