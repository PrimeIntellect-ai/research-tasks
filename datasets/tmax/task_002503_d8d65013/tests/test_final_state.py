# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_debug_report():
    report_path = "/home/user/debug_report.txt"
    assert os.path.isfile(report_path), f"Missing debug report: {report_path}"
    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, got {len(lines)}"
    assert lines[0] == "liblegacy_parser.so.4", f"Incorrect shared library in debug report: {lines[0]}"
    assert lines[1] == "asset_8921.asset", f"Incorrect last processed asset in debug report: {lines[1]}"

def test_filter_script_adversarial_corpus():
    script_path = "/home/user/filter_assets.sh"
    assert os.path.isfile(script_path), f"Missing filter script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Filter script is not executable: {script_path}"

    evil_dir = "/app/verifier_assets/evil"
    clean_dir = "/app/verifier_assets/clean"

    with tempfile.TemporaryDirectory() as evil_out, tempfile.TemporaryDirectory() as clean_out:
        # Run script on evil corpus
        result_evil = subprocess.run([script_path, evil_dir, evil_out], capture_output=True, text=True)
        assert result_evil.returncode == 0, f"Script failed on evil corpus: {result_evil.stderr}"

        # Run script on clean corpus
        result_clean = subprocess.run([script_path, clean_dir, clean_out], capture_output=True, text=True)
        assert result_clean.returncode == 0, f"Script failed on clean corpus: {result_clean.stderr}"

        evil_files = set(os.listdir(evil_dir))
        clean_files = set(os.listdir(clean_dir))

        evil_out_files = set(os.listdir(evil_out))
        clean_out_files = set(os.listdir(clean_out))

        bypassed_evil = evil_out_files.intersection(evil_files)
        if bypassed_evil:
            pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")

        missing_clean = clean_files - clean_out_files
        if missing_clean:
            pytest.fail(f"{len(missing_clean)} of {len(clean_files)} clean modified/missing: {', '.join(missing_clean)}")