# test_final_state.py
import os
import subprocess

def test_sim_engine_fixed_exists_and_executable():
    path = "/home/user/sim_engine_fixed"
    assert os.path.isfile(path), f"{path} does not exist. Did you recompile the code?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_sim_engine_fixed_runs_successfully():
    path = "/home/user/sim_engine_fixed"
    assert os.path.isfile(path), f"{path} does not exist."

    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed to run, exited with code {result.returncode}."
    assert "Speed: 5e+42" in result.stdout, f"Expected 'Speed: 5e+42' in output, but got: {result.stdout}"

def test_report_content():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you create the report?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "SESSION_ID:TXN-8842-OMEGA-PROTOCOL",
        "CRASH_FUNCTION:calculate_speed",
        "FIXED_PARAM:delta"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report content mismatch.\nExpected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )

def test_sim_engine_cpp_fixed():
    path = "/home/user/src/sim_engine.cpp"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "float delta" not in content, "The vulnerable parameter 'float delta' was not changed in the source code."