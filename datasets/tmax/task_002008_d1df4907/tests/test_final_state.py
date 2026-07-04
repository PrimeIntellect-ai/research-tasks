# test_final_state.py

import os
import glob
import json
import subprocess
import tempfile
import pytest

def test_sanitizer_executable_exists():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer binary not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer binary at {sanitizer_path} is not executable"

def test_libsvd_compiled():
    lib_path = "/app/svdlibc/libsvd.a"
    assert os.path.isfile(lib_path), f"Static library {lib_path} was not compiled successfully."

def test_clean_corpus_preserved():
    clean_files = glob.glob("/hidden/eval/clean/*")
    assert len(clean_files) > 0, "No clean corpus files found in /hidden/eval/clean/"

    anchors_path = "/home/user/corpora/anchors.txt"
    bypassed = []

    for f in clean_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_txt = os.path.join(tmpdir, "out.txt")
            out_json = os.path.join(tmpdir, "log.json")
            cmd = ["/home/user/sanitizer", f, anchors_path, out_txt, out_json]

            res = subprocess.run(cmd, capture_output=True)
            if res.returncode != 0:
                bypassed.append(f"{os.path.basename(f)} (crashed)")
                continue

            if not os.path.exists(out_json):
                bypassed.append(f"{os.path.basename(f)} (no json log)")
                continue

            try:
                with open(out_json, "r") as jf:
                    data = json.load(jf)
                if data.get("rejected_vectors", -1) != 0:
                    bypassed.append(os.path.basename(f))
            except Exception:
                bypassed.append(f"{os.path.basename(f)} (invalid json)")

    assert len(bypassed) == 0, f"{len(bypassed)} of {len(clean_files)} clean modified: {', '.join(bypassed)}"

def test_evil_corpus_rejected():
    evil_files = glob.glob("/hidden/eval/evil/*")
    assert len(evil_files) > 0, "No evil corpus files found in /hidden/eval/evil/"

    anchors_path = "/home/user/corpora/anchors.txt"
    bypassed = []

    for f in evil_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_txt = os.path.join(tmpdir, "out.txt")
            out_json = os.path.join(tmpdir, "log.json")
            cmd = ["/home/user/sanitizer", f, anchors_path, out_txt, out_json]

            res = subprocess.run(cmd, capture_output=True)
            if res.returncode != 0:
                bypassed.append(f"{os.path.basename(f)} (crashed)")
                continue

            if not os.path.exists(out_json):
                bypassed.append(f"{os.path.basename(f)} (no json log)")
                continue

            try:
                with open(out_json, "r") as jf:
                    data = json.load(jf)
                # If it's an evil file, it must have rejected at least some vectors
                if data.get("rejected_vectors", 0) == 0:
                    bypassed.append(os.path.basename(f))
            except Exception:
                bypassed.append(f"{os.path.basename(f)} (invalid json)")

    assert len(bypassed) == 0, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"