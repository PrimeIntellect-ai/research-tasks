# test_final_state.py
import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/primer_filter.py"
TARGET = "ATGCGTACGTAGCTAGCTAGCTGATCGATCGTAGCTAGCTAGCTGACTGACTAGCTAGCTAG"
MC_ITERS = "5000"
THRESH = "0.15"

CLEAN_DIR = "/app/corpora/clean/"
EVIL_DIR = "/app/corpora/evil/"

def parse_fasta(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        lines = f.readlines()
    seqs = []
    curr_seq = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if curr_seq:
                seqs.append("".join(curr_seq))
                curr_seq = []
        else:
            curr_seq.append(line)
    if curr_seq:
        seqs.append("".join(curr_seq))
    return seqs

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Missing required script: {SCRIPT_PATH}"

def test_clean_corpus_preserved():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.fasta')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for fname in clean_files:
        input_path = os.path.join(CLEAN_DIR, fname)
        with tempfile.NamedTemporaryFile(suffix=".fasta", delete=False) as tmp:
            output_path = tmp.name

        cmd = [
            "python3", SCRIPT_PATH,
            "--input", input_path,
            "--output", output_path,
            "--target", TARGET,
            "--mc-iters", MC_ITERS,
            "--thresh", THRESH
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append((fname, f"Script crashed with returncode {result.returncode}"))
            continue

        input_seqs = parse_fasta(input_path)
        output_seqs = parse_fasta(output_path)

        if input_seqs != output_seqs:
            failed_files.append((fname, "Output sequences do not match input sequences (clean sequences were modified or rejected)."))

        if os.path.exists(output_path):
            os.remove(output_path)

    if failed_files:
        msg = f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected.\n"
        for fname, err in failed_files:
            msg += f" - {fname}: {err}\n"
        pytest.fail(msg)

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.fasta')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for fname in evil_files:
        input_path = os.path.join(EVIL_DIR, fname)
        with tempfile.NamedTemporaryFile(suffix=".fasta", delete=False) as tmp:
            output_path = tmp.name

        cmd = [
            "python3", SCRIPT_PATH,
            "--input", input_path,
            "--output", output_path,
            "--target", TARGET,
            "--mc-iters", MC_ITERS,
            "--thresh", THRESH
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append((fname, f"Script crashed with returncode {result.returncode}"))
            continue

        output_seqs = parse_fasta(output_path)

        if len(output_seqs) > 0:
            failed_files.append((fname, "Output sequences are not empty (evil sequences bypassed)."))

        if os.path.exists(output_path):
            os.remove(output_path)

    if failed_files:
        msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed.\n"
        for fname, err in failed_files:
            msg += f" - {fname}: {err}\n"
        pytest.fail(msg)