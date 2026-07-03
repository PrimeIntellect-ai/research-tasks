# test_final_state.py

import os
import subprocess
import tempfile
import pytest

CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
MANIFEST = "/home/user/pza_tool/Cargo.toml"
PREFIX = "OMEGA_99"

def run_tool(pza_path, output_dir):
    cmd = [
        "cargo", "run",
        "--manifest-path", MANIFEST,
        "--",
        pza_path,
        output_dir,
        PREFIX
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_evil_corpus_rejected():
    assert os.path.exists(MANIFEST), f"Rust project manifest not found at {MANIFEST}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.pza')]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []

    for evil_file in evil_files:
        pza_path = os.path.join(EVIL_CORPUS, evil_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            returncode, stdout, stderr = run_tool(pza_path, tmpdir)
            if returncode != 1:
                bypassed.append((evil_file, returncode, stderr))

    if bypassed:
        details = "\n".join([f"{f}: exit code {c}" for f, c, e in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed:\n{details}")

def test_clean_corpus_accepted():
    assert os.path.exists(MANIFEST), f"Rust project manifest not found at {MANIFEST}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.pza')]
    assert len(clean_files) > 0, "No files found in clean corpus."

    failed = []

    for clean_file in clean_files:
        pza_path = os.path.join(CLEAN_CORPUS, clean_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            returncode, stdout, stderr = run_tool(pza_path, tmpdir)
            if returncode != 0:
                failed.append((clean_file, returncode, stderr))
            else:
                # Check if extracted files have the prefix
                extracted = []
                for root, dirs, files in os.walk(tmpdir):
                    for file in files:
                        extracted.append(file)

                if not extracted:
                    failed.append((clean_file, "No files extracted", ""))
                else:
                    for f in extracted:
                        if not f.startswith(f"{PREFIX}_"):
                            failed.append((clean_file, f"File {f} missing prefix {PREFIX}_", ""))
                            break

    if failed:
        details = "\n".join([f"{f}: {c} - {e}" for f, c, e in failed])
        pytest.fail(f"{len(failed)} of {len(clean_files)} clean modified or failed:\n{details}")