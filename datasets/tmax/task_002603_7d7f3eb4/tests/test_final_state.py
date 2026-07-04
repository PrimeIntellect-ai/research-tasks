# test_final_state.py

import os
import subprocess
import pytest

def test_libcsvparser_built():
    lib_path = '/app/csv-parser-2.1.3/libcsvparser.a'
    assert os.path.isfile(lib_path), f"{lib_path} is missing. Did you fix the Makefile and run make?"

def test_artifact_filter_executable_exists():
    exe_path = '/home/user/workspace/artifact_filter'
    assert os.path.isfile(exe_path), f"{exe_path} is missing. Did you compile your C++ program?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_clean_corpus_accepted():
    exe_path = '/home/user/workspace/artifact_filter'
    metadata_path = '/data/clean_corpus/metadata.csv'
    embeddings_path = '/data/clean_corpus/embeddings.bin'

    result = subprocess.run([exe_path, metadata_path, embeddings_path], capture_output=True, text=True)
    assert result.returncode == 0, f"artifact_filter failed with return code {result.returncode} on clean corpus.\nStderr: {result.stderr}"

    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert len(lines) > 0, "No output produced for clean corpus."

    rejected = []
    for line in lines:
        if not line.endswith(',ACCEPT'):
            rejected.append(line)

    assert not rejected, f"{len(rejected)} of {len(lines)} clean artifacts rejected or modified. Offending lines: {rejected}"

def test_evil_corpus_rejected():
    exe_path = '/home/user/workspace/artifact_filter'
    metadata_path = '/data/evil_corpus/metadata.csv'
    embeddings_path = '/data/evil_corpus/embeddings.bin'

    result = subprocess.run([exe_path, metadata_path, embeddings_path], capture_output=True, text=True)
    assert result.returncode == 0, f"artifact_filter failed with return code {result.returncode} on evil corpus.\nStderr: {result.stderr}"

    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert len(lines) > 0, "No output produced for evil corpus."

    accepted = []
    for line in lines:
        if not line.endswith(',REJECT'):
            accepted.append(line)

    assert not accepted, f"{len(accepted)} of {len(lines)} evil artifacts bypassed rejection. Offending lines: {accepted}"