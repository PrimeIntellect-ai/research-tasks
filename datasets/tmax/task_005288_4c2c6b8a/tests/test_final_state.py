# test_final_state.py
import os
import subprocess
import re

def test_deterministic_score_file():
    path = "/home/user/deterministic_score.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    try:
        float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid float. Found: '{content}'"

def test_script_uses_pool():
    path = "/home/user/spectral_primer_score.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "Pool" in content, "The script must preserve the use of multiprocessing.Pool."

def test_script_deterministic_output():
    path = "/home/user/spectral_primer_score.py"
    outputs = []
    for i in range(5):
        result = subprocess.run(["python3", path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script execution failed on run {i+1}:\n{result.stderr}"

        match = re.search(r"Total Score:\s*([0-9.eE+-]+)", result.stdout)
        assert match is not None, f"Could not find 'Total Score: <number>' in script output on run {i+1}. Output was:\n{result.stdout}"
        outputs.append(match.group(1))

    assert len(set(outputs)) == 1, f"Script output is not deterministic. Outputs over 5 runs: {outputs}"

    score_path = "/home/user/deterministic_score.txt"
    with open(score_path, "r") as f:
        saved_score = f.read().strip()

    assert float(saved_score) == float(outputs[0]), f"Saved score '{saved_score}' in {score_path} does not match script output '{outputs[0]}'."