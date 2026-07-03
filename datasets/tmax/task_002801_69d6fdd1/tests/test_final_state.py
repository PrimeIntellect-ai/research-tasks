# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/process_translations.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def run_script(input_dir, output_dir):
    """Run the student's script and return the CompletedProcess."""
    return subprocess.run(
        ["python", SCRIPT_PATH, input_dir, output_dir],
        capture_output=True,
        text=True
    )

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_clean_corpus_preserved():
    with tempfile.TemporaryDirectory() as tmp_out:
        result = run_script(CLEAN_CORPUS_DIR, tmp_out)
        assert result.returncode == 0, f"Script failed on clean corpus. Stderr: {result.stderr}"

        clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".json")]
        processed_files = [f for f in os.listdir(tmp_out) if f.endswith(".json")]

        missing = set(clean_files) - set(processed_files)
        assert not missing, f"{len(missing)} of {len(clean_files)} clean files were modified/rejected unexpectedly. Missing: {missing}"

        # Verify content of a known clean file
        for filename in clean_files:
            in_path = os.path.join(CLEAN_CORPUS_DIR, filename)
            out_path = os.path.join(tmp_out, filename)

            with open(in_path, "r") as f:
                in_data = json.load(f)

            with open(out_path, "r") as f:
                out_data = json.load(f)

            assert "id" in out_data and out_data["id"] == in_data["id"]
            assert "iso_timestamp" in out_data
            assert "T" in out_data["iso_timestamp"] # ISO 8601 check
            assert "tokenized" in out_data
            assert isinstance(out_data["tokenized"], list)
            assert len(out_data["tokenized"]) > 0

def test_evil_corpus_rejected():
    with tempfile.TemporaryDirectory() as tmp_out:
        result = run_script(EVIL_CORPUS_DIR, tmp_out)
        assert result.returncode == 0, f"Script failed on evil corpus. Stderr: {result.stderr}"

        evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".json")]
        processed_files = [f for f in os.listdir(tmp_out) if f.endswith(".json")]

        assert not processed_files, f"{len(processed_files)} of {len(evil_files)} evil files bypassed the filter. Offending output files: {processed_files}"

def test_vendored_package_fixed():
    utils_py = "/app/vendored/loc-math-parser-0.1.0/loc_math_parser/utils.py"
    assert os.path.isfile(utils_py), f"File {utils_py} is missing."

    with open(utils_py, "r") as f:
        content = f.read()

    assert "strptime" in content, f"The typo in {utils_py} was not fixed to 'strptime'."
    assert "strp_time" not in content, f"The typo 'strp_time' is still present in {utils_py}."