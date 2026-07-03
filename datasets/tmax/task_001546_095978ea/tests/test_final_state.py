# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_detect_go_exists():
    assert os.path.isfile("/home/user/detect.go"), "/home/user/detect.go does not exist."

def test_mcparser_fixed():
    path = "/app/mcparser/parser.go"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "[]flot64" not in content, "The typo '[]flot64' is still present in parser.go."
    assert "[]float64" in content, "The return type was not fixed to '[]float64'."

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.bin"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.bin"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        res = subprocess.run(
            ["go", "run", "/home/user/detect.go", f],
            cwd="/home/user",
            capture_output=True,
            text=True
        )
        if res.returncode != 0 or res.stdout.strip() != "EVIL":
            evil_bypassed.append(os.path.basename(f))

    for f in clean_files:
        res = subprocess.run(
            ["go", "run", "/home/user/detect.go", f],
            cwd="/home/user",
            capture_output=True,
            text=True
        )
        if res.returncode != 0 or res.stdout.strip() != "CLEAN":
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))