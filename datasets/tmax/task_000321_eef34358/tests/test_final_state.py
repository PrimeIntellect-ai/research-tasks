# test_final_state.py
import os
import json
import shutil
import subprocess
import tempfile
import pytest

def test_jwt_filter_behavior():
    script_path = "/home/user/jwt_filter.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    clean_corpus_dir = "/grader/corpus/clean"
    evil_corpus_dir = "/grader/corpus/evil"

    assert os.path.exists(clean_corpus_dir), f"Grader clean corpus missing: {clean_corpus_dir}"
    assert os.path.exists(evil_corpus_dir), f"Grader evil corpus missing: {evil_corpus_dir}"

    clean_files = os.listdir(clean_corpus_dir)
    evil_files = os.listdir(evil_corpus_dir)

    with tempfile.TemporaryDirectory() as tmp_input_dir:
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            output_json_path = os.path.join(tmp_output_dir, "output_log.json")

            # Copy all files into a single input directory
            for f in clean_files:
                shutil.copy(os.path.join(clean_corpus_dir, f), os.path.join(tmp_input_dir, f))
            for f in evil_files:
                shutil.copy(os.path.join(evil_corpus_dir, f), os.path.join(tmp_input_dir, f))

            # Run the student's script
            result = subprocess.run(
                ["python3", script_path, tmp_input_dir, output_json_path],
                capture_output=True,
                text=True
            )

            assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
            assert os.path.exists(output_json_path), "Script did not produce the expected output JSON file."

            with open(output_json_path, "r") as f:
                try:
                    output_data = json.load(f)
                except json.JSONDecodeError:
                    pytest.fail("Output file is not valid JSON.")

            clean_bypassed = []
            evil_bypassed = []

            # Check clean corpus (should be false)
            for f in clean_files:
                if f not in output_data:
                    clean_bypassed.append(f"{f} (missing in output)")
                elif output_data[f] is not False:
                    clean_bypassed.append(f)

            # Check evil corpus (should be true)
            for f in evil_files:
                if f not in output_data:
                    evil_bypassed.append(f"{f} (missing in output)")
                elif output_data[f] is not True:
                    evil_bypassed.append(f)

            error_msgs = []
            if evil_bypassed:
                error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
            if clean_bypassed:
                error_msgs.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified/flagged: {', '.join(clean_bypassed[:5])}{'...' if len(clean_bypassed) > 5 else ''}")

            if error_msgs:
                pytest.fail(" | ".join(error_msgs))