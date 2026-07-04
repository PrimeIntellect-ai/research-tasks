# test_final_state.py

import os
import sys
import json
import re
import subprocess
import tempfile
import shutil
from collections import defaultdict, deque

def test_calculator_fixed():
    path = "/app/vendored/py-rolling-stats-0.1.0/py_rolling_stats/calculator.py"
    assert os.path.isfile(path), f"calculator.py is missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "MAX_WINDOW_SIZE" in content, "The typo 'MAX_WINDW_SIZE' was not fixed to 'MAX_WINDOW_SIZE'."
    assert "MAX_WINDW_SIZE" not in content, "The typo 'MAX_WINDW_SIZE' is still present in calculator.py."

def test_script_exists():
    script_path = "/home/user/process_configs.py"
    assert os.path.isfile(script_path), f"Processor script missing at {script_path}"

def mask_content(text):
    # Mask IPv4
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IPV4]', text)
    # Mask AWS Key
    text = re.sub(r'\bAKIA[A-Z0-9]{16}\b', '[AWS_KEY]', text)
    # Mask password=...
    text = re.sub(r'password=\S+', 'password=[PASSWORD]', text)
    # Mask "password": "..."
    text = re.sub(r'"password"\s*:\s*"[^"]*"', '"password": "[PASSWORD]"', text)
    return text

class ExpectedRollingStats:
    def __init__(self):
        self.history = defaultdict(lambda: deque(maxlen=5))

    def add_and_check(self, server_id, diff_size):
        self.history[server_id].append(diff_size)
        avg = sum(self.history[server_id]) / len(self.history[server_id])
        return avg > 50.0

def run_student_script(input_dir, output_dir):
    script_path = "/home/user/process_configs.py"
    env = os.environ.copy()
    env["MAX_WINDOW_SIZE"] = "5"
    result = subprocess.run(
        [sys.executable, script_path, input_dir, output_dir],
        capture_output=True,
        text=True,
        env=env
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def process_corpus_and_verify(corpus_path, is_evil):
    with tempfile.TemporaryDirectory() as temp_out:
        run_student_script(corpus_path, temp_out)

        input_files = [f for f in os.listdir(corpus_path) if f.endswith('.jsonl')]
        output_files = [f for f in os.listdir(temp_out) if f.endswith('.jsonl')]

        assert set(input_files) == set(output_files), "Output files do not match input files."

        stats = ExpectedRollingStats()
        failed_files = []

        for fname in input_files:
            in_path = os.path.join(corpus_path, fname)
            out_path = os.path.join(temp_out, fname)

            with open(in_path, 'r') as fin, open(out_path, 'r') as fout:
                in_lines = fin.read().splitlines()
                out_lines = fout.read().splitlines()

                if len(in_lines) != len(out_lines):
                    failed_files.append(fname)
                    continue

                file_ok = True
                for line_idx, (in_line, out_line) in enumerate(zip(in_lines, out_lines)):
                    if not in_line.strip():
                        continue

                    try:
                        in_obj = json.loads(in_line)
                        out_obj = json.loads(out_line)
                    except json.JSONDecodeError:
                        file_ok = False
                        break

                    server_id = in_obj.get("server_id")
                    diff_size = in_obj.get("diff_size", 0)
                    expected_anomaly = stats.add_and_check(server_id, diff_size)

                    if out_obj.get("anomaly") != expected_anomaly:
                        file_ok = False
                        break

                    expected_content = mask_content(in_obj.get("content", ""))
                    if out_obj.get("content") != expected_content:
                        file_ok = False
                        break

                    # For clean corpus, ensure content is completely unchanged
                    if not is_evil:
                        if out_obj.get("content") != in_obj.get("content"):
                            file_ok = False
                            break

                if not file_ok:
                    failed_files.append(fname)

        return failed_files, len(input_files)

def test_clean_corpus():
    clean_path = "/home/user/corpora/clean"
    if not os.path.isdir(clean_path):
        return
    failed_files, total = process_corpus_and_verify(clean_path, is_evil=False)
    assert not failed_files, f"{len(failed_files)} of {total} clean modified/incorrect. Offending files: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_path = "/home/user/corpora/evil"
    if not os.path.isdir(evil_path):
        return
    failed_files, total = process_corpus_and_verify(evil_path, is_evil=True)
    assert not failed_files, f"{len(failed_files)} of {total} evil bypassed/incorrect. Offending files: {', '.join(failed_files)}"