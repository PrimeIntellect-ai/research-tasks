# test_final_state.py
import os
import shutil
import subprocess
import tempfile
import pytest

def test_go_binary_built():
    bin_path = "/workspace/bin/processor"
    assert os.path.isfile(bin_path), f"Go binary {bin_path} was not built."
    assert os.access(bin_path, os.X_OK), f"Go binary {bin_path} is not executable."

def test_python_filter_exists():
    script_path = "/workspace/filter.py"
    assert os.path.isfile(script_path), f"Python 3 filter script {script_path} is missing."

def test_adversarial_corpus_filtering():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"
    script_path = "/workspace/filter.py"
    true_key = "142"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    with tempfile.TemporaryDirectory() as mixed_dir, tempfile.TemporaryDirectory() as out_dir:
        evil_files = os.listdir(evil_dir)
        clean_files = os.listdir(clean_dir)

        # Prefix files to avoid any name collisions and easily track them
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(mixed_dir, f"evil_{f}"))
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(mixed_dir, f"clean_{f}"))

        cmd = [
            "python3", script_path,
            "--input", mixed_dir,
            "--output", out_dir,
            "--key", true_key
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Filter script failed with return code {result.returncode}\nStderr: {result.stderr}"

        out_files = set(os.listdir(out_dir))

        evil_bypassed = [f for f in evil_files if f"evil_{f}" in out_files]
        clean_modified = [f for f in clean_files if f"clean_{f}" not in out_files]

        err_msg = []
        if evil_bypassed:
            err_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed[:5]}")
        if clean_modified:
            err_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {clean_modified[:5]}")

        assert not err_msg, " | ".join(err_msg)