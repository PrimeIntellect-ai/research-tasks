# test_final_state.py
import os
import stat

def test_extract_script_exists_and_executable():
    script_path = "/home/user/extract.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {script_path} is not executable."

def test_summary_csv_content():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Summary CSV {summary_path} does not exist."

    expected_lines = [
        "run_1,0.85,120",
        "run_2,0.92,150",
        "run_3,0.88,110",
        "run_4,0.95,200",
        "run_5,0.79,90"
    ]

    with open(summary_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {summary_path} is incorrect or not sorted properly. Expected: {expected_lines}, Got: {actual_lines}"

def test_analyze_runs_c_and_executable():
    c_path = "/home/user/analyze_runs.c"
    exe_path = "/home/user/analyze_runs"

    assert os.path.isfile(c_path), f"C source file {c_path} does not exist."
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled file {exe_path} is not executable."

def test_best_match_output():
    best_match_path = "/home/user/best_match.txt"
    assert os.path.isfile(best_match_path), f"Output file {best_match_path} does not exist."

    with open(best_match_path, "r") as f:
        content = f.read().strip()

    assert content == "run_2", f"Expected closest match 'run_2', but got '{content}'."

def test_posterior_output():
    posterior_path = "/home/user/posterior.txt"
    assert os.path.isfile(posterior_path), f"Output file {posterior_path} does not exist."

    with open(posterior_path, "r") as f:
        content = f.read().strip()

    expected_val = "0.8028"
    assert content == expected_val, f"Expected posterior probability '{expected_val}', but got '{content}'."