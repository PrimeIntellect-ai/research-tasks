# test_final_state.py

import os
import re
import subprocess
import tempfile
import pytest

def parse_fasta(path):
    records = []
    with open(path, 'r') as f:
        header = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header is not None:
                    records.append((header, ''.join(seq)))
                header = line
                seq = []
            else:
                seq.append(line)
        if header is not None:
            records.append((header, ''.join(seq)))
    return records

def is_evil(seq):
    if 'N' in seq.upper():
        return True
    if re.search(r'(.)\1{20,}', seq):
        return True
    return False

def test_optimal_k_computed():
    optimal_k_path = "/home/user/optimal_k.txt"
    assert os.path.exists(optimal_k_path), f"Missing {optimal_k_path}"

    with open(optimal_k_path, 'r') as f:
        content = f.read().strip()

    assert content == "31", f"Expected optimal k to be 31, but found '{content}' in {optimal_k_path}"

def test_scripts_executable():
    sanitize_script = "/home/user/sanitize_reads.sh"
    find_script = "/home/user/find_optimal_k.sh"

    assert os.path.exists(sanitize_script), f"Missing {sanitize_script}"
    assert os.access(sanitize_script, os.X_OK), f"{sanitize_script} is not executable"

    assert os.path.exists(find_script), f"Missing {find_script}"
    assert os.access(find_script, os.X_OK), f"{find_script} is not executable"

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"
    script_path = "/home/user/sanitize_reads.sh"

    assert os.path.exists(script_path), f"Missing {script_path}"

    evil_bypassed = 0
    evil_total = 0
    clean_modified = 0
    clean_total = 0

    evil_offenders = set()
    clean_offenders = set()

    # Check evil corpus
    if os.path.exists(evil_dir):
        for fname in os.listdir(evil_dir):
            if not fname.endswith('.fasta'): continue
            path = os.path.join(evil_dir, fname)

            with tempfile.NamedTemporaryFile(suffix='.fasta') as tmp:
                subprocess.run([script_path, path, tmp.name], check=True)
                out_records = parse_fasta(tmp.name)

            in_records = parse_fasta(path)
            out_dict = dict(out_records)

            for header, seq in in_records:
                if is_evil(seq):
                    evil_total += 1
                    if header in out_dict:
                        evil_bypassed += 1
                        evil_offenders.add(fname)
                else:
                    clean_total += 1
                    if header not in out_dict or out_dict[header] != seq:
                        clean_modified += 1
                        clean_offenders.add(fname)

    # Check clean corpus
    if os.path.exists(clean_dir):
        for fname in os.listdir(clean_dir):
            if not fname.endswith('.fasta'): continue
            path = os.path.join(clean_dir, fname)

            with tempfile.NamedTemporaryFile(suffix='.fasta') as tmp:
                subprocess.run([script_path, path, tmp.name], check=True)
                out_records = parse_fasta(tmp.name)

            in_records = parse_fasta(path)
            out_dict = dict(out_records)

            for header, seq in in_records:
                clean_total += 1
                if header not in out_dict or out_dict[header] != seq:
                    clean_modified += 1
                    clean_offenders.add(fname)

    errors = []
    if evil_bypassed > 0:
        errors.append(f"{evil_bypassed} of {evil_total} evil bypassed. Offending files: {', '.join(evil_offenders)}")
    if clean_modified > 0:
        errors.append(f"{clean_modified} of {clean_total} clean modified. Offending files: {', '.join(clean_offenders)}")

    if errors:
        pytest.fail(" ; ".join(errors))