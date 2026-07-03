# test_final_state.py
import os
import subprocess
import tempfile
import shutil
import pytest

def test_pulse_count():
    pulse_file = "/home/user/pulse_count.txt"
    assert os.path.isfile(pulse_file), f"File {pulse_file} does not exist."
    with open(pulse_file, "r") as f:
        content = f.read().strip()
    assert content == "27", f"Expected pulse count to be 27, but got {content}."

def test_dataset_filter_executable():
    c_source = "/home/user/dataset_filter.c"
    executable = "/home/user/dataset_filter"

    assert os.path.isfile(c_source), f"Source file {c_source} does not exist."

    # Compile if not exists or just to be sure
    if not os.path.isfile(executable):
        subprocess.run(["gcc", "-O2", c_source, "-o", executable], check=True)

    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"Executable {executable} is not executable."

def test_dataset_filter_clean_corpus():
    executable = "/home/user/dataset_filter"
    clean_in = "/app/corpus/clean"

    if not os.path.isfile(executable):
        subprocess.run(["gcc", "-O2", "/home/user/dataset_filter.c", "-o", executable], check=True)

    with tempfile.TemporaryDirectory() as clean_out:
        clean_manifest = os.path.join(clean_out, "manifest.txt")

        result = subprocess.run([executable, clean_in, clean_out, clean_manifest], capture_output=True, text=True)
        assert result.returncode == 0, f"dataset_filter failed on clean corpus: {result.stderr}"

        expected_files = set(os.listdir(clean_in))
        actual_files = set(os.listdir(clean_out)) - {"manifest.txt"}

        missing = expected_files - actual_files
        assert not missing, f"{len(missing)} of {len(expected_files)} clean files modified/rejected: {missing}"

        # Verify file contents are unchanged
        for f in expected_files:
            in_path = os.path.join(clean_in, f)
            out_path = os.path.join(clean_out, f)
            with open(in_path, "rb") as fin, open(out_path, "rb") as fout:
                assert fin.read() == fout.read(), f"Clean file {f} was modified during copy."

def test_dataset_filter_evil_corpus():
    executable = "/home/user/dataset_filter"
    evil_in = "/app/corpus/evil"

    if not os.path.isfile(executable):
        subprocess.run(["gcc", "-O2", "/home/user/dataset_filter.c", "-o", executable], check=True)

    with tempfile.TemporaryDirectory() as evil_out:
        evil_manifest = os.path.join(evil_out, "manifest.txt")

        result = subprocess.run([executable, evil_in, evil_out, evil_manifest], capture_output=True, text=True)
        assert result.returncode == 0, f"dataset_filter failed on evil corpus: {result.stderr}"

        actual_files = set(os.listdir(evil_out)) - {"manifest.txt"}
        expected_files = set(os.listdir(evil_in))

        assert not actual_files, f"{len(actual_files)} of {len(expected_files)} evil files bypassed: {actual_files}"