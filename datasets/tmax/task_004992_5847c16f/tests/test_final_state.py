# test_final_state.py

import os
import glob
import subprocess
import shutil
import pytest

def read_fasta(file_path):
    """Simple FASTA parser returning a list of (header, sequence) tuples."""
    sequences = []
    if not os.path.exists(file_path):
        return sequences

    with open(file_path, 'r') as f:
        header = None
        seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    sequences.append((header, "".join(seq)))
                header = line
                seq = []
            else:
                seq.append(line)
        if header is not None:
            sequences.append((header, "".join(seq)))
    return sequences

def test_filter_script_exists():
    assert os.path.isfile("/home/user/filter_primers.py"), "The script /home/user/filter_primers.py does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/filter_primers.py"
    clean_in = "/home/user/corpus/clean"
    evil_in = "/home/user/corpus/evil"
    clean_out = "/tmp/out_clean"
    evil_out = "/tmp/out_evil"

    os.makedirs(clean_out, exist_ok=True)
    os.makedirs(evil_out, exist_ok=True)

    # Run on clean corpus
    result_clean = subprocess.run(
        ["python3", script_path, clean_in, clean_out],
        capture_output=True, text=True
    )
    assert result_clean.returncode == 0, f"Script failed on clean corpus:\n{result_clean.stderr}"

    # Run on evil corpus
    result_evil = subprocess.run(
        ["python3", script_path, evil_in, evil_out],
        capture_output=True, text=True
    )
    assert result_evil.returncode == 0, f"Script failed on evil corpus:\n{result_evil.stderr}"

    # Verify clean corpus (100% preserved)
    clean_files = glob.glob(os.path.join(clean_in, "*.fasta"))
    assert len(clean_files) > 0, "No clean corpus files found to test."

    clean_modified = []
    for cf in clean_files:
        basename = os.path.basename(cf)
        out_f = os.path.join(clean_out, basename)

        in_seqs = read_fasta(cf)
        out_seqs = read_fasta(out_f)

        if in_seqs != out_seqs:
            clean_modified.append(basename)

    # Verify evil corpus (100% rejected)
    evil_files = glob.glob(os.path.join(evil_in, "*.fasta"))
    assert len(evil_files) > 0, "No evil corpus files found to test."

    evil_bypassed = []
    for ef in evil_files:
        basename = os.path.basename(ef)
        out_f = os.path.join(evil_out, basename)

        out_seqs = read_fasta(out_f)
        if len(out_seqs) > 0:
            evil_bypassed.append(basename)

    error_msgs = []
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))