# test_final_state.py

import os
import stat
import subprocess
import tempfile

def test_filter_script_exists():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_filter_behavior_on_corpora():
    script_path = "/home/user/filter.sh"
    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus), f"Clean corpus missing at {clean_corpus}"
    assert os.path.isdir(evil_corpus), f"Evil corpus missing at {evil_corpus}"

    expected_signature = "Signature: BLUE JAY VOCALIZATION IN NORTHERN WOODS"

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run script on clean corpus
        res_clean = subprocess.run(
            ["bash", script_path, clean_corpus, clean_out],
            capture_output=True, text=True
        )
        assert res_clean.returncode == 0, f"Script failed on clean corpus. stderr: {res_clean.stderr}"

        # Run script on evil corpus
        res_evil = subprocess.run(
            ["bash", script_path, evil_corpus, evil_out],
            capture_output=True, text=True
        )
        assert res_evil.returncode == 0, f"Script failed on evil corpus. stderr: {res_evil.stderr}"

        clean_in_files = set(os.listdir(clean_corpus))
        clean_out_files = set(os.listdir(clean_out))

        evil_in_files = set(os.listdir(evil_corpus))
        evil_out_files = set(os.listdir(evil_out))

        # 1. Check clean files are preserved
        missing_clean = clean_in_files - clean_out_files
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_in_files)} clean files were incorrectly rejected: {', '.join(missing_clean)}"

        # 2. Check clean files are properly transformed (original content + signature)
        modified_clean = []
        for f in clean_in_files:
            in_path = os.path.join(clean_corpus, f)
            out_path = os.path.join(clean_out, f)
            with open(in_path, 'r') as f_in, open(out_path, 'r') as f_out:
                in_content = f_in.read()
                out_content = f_out.read()

                # Strip trailing newlines to compare base content
                in_lines = in_content.strip('\n').split('\n')
                out_lines = out_content.strip('\n').split('\n')

                if not out_lines or out_lines[-1] != expected_signature:
                    modified_clean.append(f)
                elif out_lines[:-1] != in_lines:
                    modified_clean.append(f)

        assert not modified_clean, f"{len(modified_clean)} of {len(clean_in_files)} clean files were improperly modified or missing the correct signature: {', '.join(modified_clean)}"

        # 3. Check evil files are rejected
        bypassed_evil = evil_out_files
        assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_in_files)} evil files bypassed the filter and were copied to output: {', '.join(bypassed_evil)}"