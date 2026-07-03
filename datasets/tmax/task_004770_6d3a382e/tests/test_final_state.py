# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = "/app/libkmer-svd-1.2.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "-fPIC" in content, "Makefile is still missing the -fPIC flag."
    assert "-lm" in content, "Makefile is still missing the -lm flag for math library linking."

def test_library_compiled():
    so_path = "/app/libkmer-svd-1.2.0/libkmer-svd.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled or is missing."

def test_seq_filter_exists():
    bin_path = "/home/user/seq_filter"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_evil_corpus_rejected():
    bin_path = "/home/user/seq_filter"
    evil_dir = "/home/user/data/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.fasta"))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    bypassed = []
    for f in evil_files:
        try:
            # We explicitly set LD_LIBRARY_PATH in case the binary relies on it
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = "/app/libkmer-svd-1.2.0:" + env.get("LD_LIBRARY_PATH", "")

            out = subprocess.check_output([bin_path, f], env=env, text=True, timeout=5).strip()
            if out != "REJECT":
                bypassed.append((os.path.basename(f), out))
        except subprocess.CalledProcessError as e:
            # If the process returns non-zero, it might be a crash or error, which is not a clean 'REJECT'
            bypassed.append((os.path.basename(f), f"Error/Crash: {e.output}"))
        except Exception as e:
            bypassed.append((os.path.basename(f), str(e)))

    if bypassed:
        details = ", ".join([f"'{f}' (output: {out})" for f, out in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {details}")

def test_clean_corpus_accepted():
    bin_path = "/home/user/seq_filter"
    clean_dir = "/home/user/data/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.fasta"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."

    modified = []
    for f in clean_files:
        try:
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = "/app/libkmer-svd-1.2.0:" + env.get("LD_LIBRARY_PATH", "")

            out = subprocess.check_output([bin_path, f], env=env, text=True, timeout=5).strip()
            if out != "ACCEPT":
                modified.append((os.path.basename(f), out))
        except subprocess.CalledProcessError as e:
            modified.append((os.path.basename(f), f"Error/Crash: {e.output}"))
        except Exception as e:
            modified.append((os.path.basename(f), str(e)))

    if modified:
        details = ", ".join([f"'{f}' (output: {out})" for f, out in modified])
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected: {details}")