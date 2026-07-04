# test_final_state.py
import os

def test_executable_exists():
    executable = "/home/user/bin/seq_density"
    assert os.path.isfile(executable), f"Executable missing: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_report_exists_and_content():
    report_file = "/home/user/analysis_report.txt"
    assert os.path.isfile(report_file), f"Report file missing: {report_file}"

    with open(report_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Report file should have exactly 2 non-empty lines, found {len(lines)}"

    assert lines[0] == "Optimal_W: 20", f"First line incorrect. Expected 'Optimal_W: 20', got '{lines[0]}'"
    assert lines[1] == "Most_Divergent_Seq: Seq2", f"Second line incorrect. Expected 'Most_Divergent_Seq: Seq2', got '{lines[1]}'"