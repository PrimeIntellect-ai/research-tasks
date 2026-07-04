# test_final_state.py
import os
import json
import subprocess

def test_c_source_exists():
    assert os.path.isfile("/home/user/simulate_latency.c"), "C simulator source code is missing."

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.sh"), "Bash pipeline script is missing."

def test_data_files_exist():
    assert os.path.isfile("/home/user/data_A.txt"), "data_A.txt is missing."
    assert os.path.isfile("/home/user/data_B.txt"), "data_B.txt is missing."

def test_venv_exists():
    assert os.path.isdir("/home/user/venv"), "Python virtual environment directory is missing."
    assert os.path.isfile("/home/user/venv/bin/python"), "Python executable not found in venv."

def test_analyze_script_exists():
    assert os.path.isfile("/home/user/analyze.py"), "Python analysis script is missing."

def test_stats_json_exists():
    assert os.path.isfile("/home/user/stats.json"), "stats.json is missing."

def test_stats_json_content():
    # Verify the venv has scipy installed and compute ground truth
    script = """
import sys
import json
try:
    from scipy import stats
except ImportError:
    print("SCIPY_MISSING")
    sys.exit(0)

def my_rand(state):
    state = (state * 1103515245 + 12345) & 0x7fffffff
    return state

def run_mode(mode, seed, n):
    state = seed
    total = 0.0
    for _ in range(n):
        state = my_rand(state)
        if mode == 'A':
            total += (state % 100) / 10.0
        else:
            total += (state % 105) / 10.0
    return total

mode_a = [run_mode('A', s, 1000) for s in range(1, 51)]
mode_b = [run_mode('B', s, 1000) for s in range(1, 51)]

res = stats.ttest_ind(mode_a, mode_b, equal_var=False)
print(json.dumps({
    "t_statistic": round(float(res.statistic), 4),
    "p_value": round(float(res.pvalue), 4)
}))
"""
    result = subprocess.run(["/home/user/venv/bin/python", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run ground truth script using the student's venv."

    stdout = result.stdout.strip()
    assert stdout != "SCIPY_MISSING", "scipy is not installed in the virtual environment."

    try:
        expected_data = json.loads(stdout)
    except json.JSONDecodeError:
        assert False, f"Failed to parse ground truth JSON. Output was: {stdout}"

    try:
        with open("/home/user/stats.json", "r") as f:
            student_data = json.load(f)
    except Exception as e:
        assert False, f"Failed to read or parse /home/user/stats.json: {e}"

    assert "t_statistic" in student_data, "t_statistic missing from stats.json"
    assert "p_value" in student_data, "p_value missing from stats.json"

    assert student_data["t_statistic"] == expected_data["t_statistic"], f"Expected t_statistic {expected_data['t_statistic']}, got {student_data['t_statistic']}"
    assert student_data["p_value"] == expected_data["p_value"], f"Expected p_value {expected_data['p_value']}, got {student_data['p_value']}"