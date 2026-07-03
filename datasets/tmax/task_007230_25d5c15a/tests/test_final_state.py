# test_final_state.py
import os
import ast
import subprocess

def test_fixed_output_file_exists():
    """Check that the fixed_output.txt file exists."""
    output_path = "/home/user/uptime_monitor/fixed_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist. Did you save the output?"

def test_fixed_output_content():
    """Check that the fixed_output.txt contains the correct final_uptime_score."""
    output_path = "/home/user/uptime_monitor/fixed_output.txt"
    with open(output_path, "r") as f:
        content = f.read().strip()

    assert "0.9902" in content, f"Expected to find '0.9902' in {output_path}, but found: {content}"

    # Try to parse as dict if possible
    try:
        parsed = ast.literal_eval(content)
        assert isinstance(parsed, dict), "Output should be a dictionary"
        assert "final_uptime_score" in parsed, "Dictionary must contain 'final_uptime_score'"
        assert parsed["final_uptime_score"] == 0.9902, f"Expected score 0.9902, got {parsed['final_uptime_score']}"
    except (SyntaxError, ValueError):
        # If it's not a valid dict, just rely on the string check above
        pass

def test_app_py_runs_successfully():
    """Check that the modified app.py runs without errors and outputs the correct result."""
    app_path = "/home/user/uptime_monitor/app.py"
    assert os.path.isfile(app_path), f"File {app_path} does not exist."

    result = subprocess.run(["python3", app_path], capture_output=True, text=True)
    assert result.returncode == 0, f"app.py crashed with error:\n{result.stderr}"

    output = result.stdout.strip()
    assert "0.9902" in output, f"app.py did not output the expected value '0.9902'. Output was: {output}"