# test_final_state.py

import os
import json
import subprocess
import tempfile
import shutil
import pytest

MIGRATOR_PATH = "/home/user/migrator.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def run_migrator(input_dir, output_dir, reject_log):
    cmd = [
        "python3", MIGRATOR_PATH,
        "--input-dir", input_dir,
        "--output-dir", output_dir,
        "--reject-log", reject_log
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_migrator_exists():
    assert os.path.isfile(MIGRATOR_PATH), f"Migrator script not found at {MIGRATOR_PATH}"

def test_adversarial_corpus_clean():
    if not os.path.isfile(MIGRATOR_PATH):
        pytest.fail("Migrator script missing.")

    with tempfile.TemporaryDirectory() as tmp_out:
        reject_log = os.path.join(tmp_out, "rejects.log")
        out_dir = os.path.join(tmp_out, "out")
        os.makedirs(out_dir)

        run_migrator(CLEAN_CORPUS_DIR, out_dir, reject_log)

        clean_files = set(os.listdir(CLEAN_CORPUS_DIR))
        out_files = set(os.listdir(out_dir))

        rejected_files = set()
        if os.path.isfile(reject_log):
            with open(reject_log, "r") as f:
                rejected_files = {line.strip() for line in f if line.strip()}

        failed_clean = []
        for cf in clean_files:
            if cf not in out_files or cf in rejected_files:
                failed_clean.append(cf)

        if failed_clean:
            pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_clean)}")

def test_adversarial_corpus_evil():
    if not os.path.isfile(MIGRATOR_PATH):
        pytest.fail("Migrator script missing.")

    with tempfile.TemporaryDirectory() as tmp_out:
        reject_log = os.path.join(tmp_out, "rejects.log")
        out_dir = os.path.join(tmp_out, "out")
        os.makedirs(out_dir)

        run_migrator(EVIL_CORPUS_DIR, out_dir, reject_log)

        evil_files = set(os.listdir(EVIL_CORPUS_DIR))
        out_files = set(os.listdir(out_dir))

        rejected_files = set()
        if os.path.isfile(reject_log):
            with open(reject_log, "r") as f:
                rejected_files = {line.strip() for line in f if line.strip()}

        bypassed_evil = []
        for ef in evil_files:
            if ef in out_files or ef not in rejected_files:
                bypassed_evil.append(ef)

        if bypassed_evil:
            pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_evil)}")

def test_video_configs_extracted_and_migrated():
    migrated_dir = "/home/user/video_configs_migrated"
    reject_log = "/home/user/video_rejects.log"

    assert os.path.isdir(migrated_dir), f"Migrated directory missing at {migrated_dir}"
    assert os.path.isfile(reject_log), f"Reject log missing at {reject_log}"

    migrated_files = os.listdir(migrated_dir)
    with open(reject_log, "r") as f:
        rejected_files = [line.strip() for line in f if line.strip()]

    assert len(migrated_files) > 0 or len(rejected_files) > 0, "No files were extracted or processed from the video."

    for mf in migrated_files:
        with open(os.path.join(migrated_dir, mf), "r") as f:
            try:
                data = json.load(f)
                assert "orchestration" in data, f"Migrated file {mf} missing 'orchestration' key"
                assert data.get("version") == "2.0.0" or data.get("version", "").startswith("2."), f"Migrated file {mf} has invalid version"
            except json.JSONDecodeError:
                pytest.fail(f"Migrated file {mf} is not valid JSON")