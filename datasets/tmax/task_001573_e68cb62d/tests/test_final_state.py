# test_final_state.py

import os
import stat
import subprocess
import tempfile
import pytest

def test_nginx_config_fixed():
    conf_path = "/app/services/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing"
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "5001" not in content, "Nginx config still contains the incorrect port 5001"
    assert "5000" in content, "Nginx config does not contain the correct port 5000"

def test_calc_spectrum_compiled():
    bin_path = "/home/user/bin/calc_spectrum"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing. Did you compile the C code?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_filter_seqs_script_exists():
    script_path = "/home/user/filter_seqs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_adversarial_corpus():
    script_path = "/home/user/filter_seqs.sh"
    clean_dir = "/app/data/clean"
    evil_dir = "/app/data/evil"

    clean_files = {f for f in os.listdir(clean_dir) if f.endswith('.h5')}
    evil_files = {f for f in os.listdir(evil_dir) if f.endswith('.h5')}

    assert clean_files, "Clean corpus is empty"
    assert evil_files, "Evil corpus is empty"

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run on clean corpus
        res_clean = subprocess.run([script_path, clean_dir, clean_out], capture_output=True, text=True)
        assert res_clean.returncode == 0, f"Script failed on clean corpus with error:\n{res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run([script_path, evil_dir, evil_out], capture_output=True, text=True)
        assert res_evil.returncode == 0, f"Script failed on evil corpus with error:\n{res_evil.stderr}"

        clean_out_files = {f for f in os.listdir(clean_out) if f.endswith('.h5')}
        evil_out_files = {f for f in os.listdir(evil_out) if f.endswith('.h5')}

        # Check clean corpus preserved
        missing_clean = clean_files - clean_out_files
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_files)} clean files modified/rejected. Missing clean files: {', '.join(missing_clean)}"

        # Check evil corpus rejected
        bypassed_evil = evil_out_files.intersection(evil_files)
        assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed. Bypassed evil files: {', '.join(bypassed_evil)}"