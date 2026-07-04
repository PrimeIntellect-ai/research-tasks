# test_final_state.py
import os
import subprocess
import glob

def test_rolling_avg():
    expected = [
        "2023-10-25T08:12:01,INC-5581,105,105.00",
        "2023-10-25T08:12:15,INC-5581,110,107.50",
        "2023-10-25T08:13:00,INC-5581,110,108.33",
        "2023-10-25T08:14:22,INC-5581,120,113.33",
        "2023-10-25T08:15:05,INC-5581,115,115.00"
    ]
    file_path = "/home/user/rolling_avg.csv"
    assert os.path.exists(file_path), f"{file_path} is missing."
    with open(file_path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    assert lines == expected, f"{file_path} content mismatch.\nExpected:\n{expected}\nGot:\n{lines}"

def test_detector_executable():
    script_path = "/home/user/detector.sh"
    assert os.path.exists(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_detector_clean_corpus():
    clean_files = glob.glob("/app/corpus/clean/*.csv")
    assert clean_files, "No clean corpus files found."

    failed = []
    for f in clean_files:
        with open(f, "r") as fin:
            expected = fin.read().strip()

        proc = subprocess.run(["/home/user/detector.sh"], input=expected, text=True, capture_output=True)
        out = proc.stdout.strip()

        if out != expected:
            failed.append(os.path.basename(f))

    assert not failed, f"{len(failed)} of {len(clean_files)} clean modified: {failed}"

def test_detector_evil_corpus():
    evil_files = glob.glob("/app/corpus/evil/*.csv")
    assert evil_files, "No evil corpus files found."

    failed = []
    for f in evil_files:
        with open(f, "r") as fin:
            content = fin.read().strip()

        proc = subprocess.run(["/home/user/detector.sh"], input=content, text=True, capture_output=True)
        out = proc.stdout.strip()

        # Evil files consist entirely of forged/malformed rows. Output should be empty.
        if out != "":
            failed.append(os.path.basename(f))

    assert not failed, f"{len(failed)} of {len(evil_files)} evil bypassed: {failed}"