# test_final_state.py
import os
import subprocess
import filecmp
import tempfile
import pytest

def test_pyjwt_typo_fixed():
    """Verify that the typo in the vendored pyjwt-custom library has been fixed."""
    path = "/app/vendored/pyjwt-custom/jwt/api_jwt.py"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "def verify_signature(" in content, "The typo was not fixed: 'def verify_signature(' not found."
    assert "def verfy_signature(" not in content, "The typo 'def verfy_signature(' is still present in the file."

def test_payload_filter_adversarial_corpus():
    """
    Test the payload_filter.py script against the clean and evil corpora.
    Ensures 100% of clean files are preserved and 100% of evil files are rejected.
    """
    script_path = "/home/user/payload_filter.py"
    assert os.path.isfile(script_path), f"Payload filter script not found at {script_path}"

    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus), f"Clean corpus missing at {clean_corpus}"
    assert os.path.isdir(evil_corpus), f"Evil corpus missing at {evil_corpus}"

    clean_files = set(os.listdir(clean_corpus))
    evil_files = set(os.listdir(evil_corpus))

    with tempfile.TemporaryDirectory() as tmp_clean_out, tempfile.TemporaryDirectory() as tmp_evil_out:
        # Execute the student's script on the clean corpus
        subprocess.run(
            ["python3", script_path, "--input-dir", clean_corpus, "--output-dir", tmp_clean_out],
            capture_output=True, text=True
        )

        # Execute the student's script on the evil corpus
        subprocess.run(
            ["python3", script_path, "--input-dir", evil_corpus, "--output-dir", tmp_evil_out],
            capture_output=True, text=True
        )

        clean_out_files = set(os.listdir(tmp_clean_out))
        evil_out_files = set(os.listdir(tmp_evil_out))

        # Analyze clean corpus results
        clean_missing = clean_files - clean_out_files
        clean_modified = []
        for f in clean_files.intersection(clean_out_files):
            src = os.path.join(clean_corpus, f)
            dst = os.path.join(tmp_clean_out, f)
            if not filecmp.cmp(src, dst, shallow=False):
                clean_modified.append(f)

        clean_failed = len(clean_missing) + len(clean_modified)

        # Analyze evil corpus results
        evil_bypassed = evil_out_files.intersection(evil_files)

        # Construct failure summary
        errors = []
        if clean_failed > 0:
            errors.append(f"{clean_failed} of {len(clean_files)} clean modified or missing. "
                          f"Missing: {list(clean_missing)}, Modified: {clean_modified}")
        if len(evil_bypassed) > 0:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. "
                          f"Bypassed basenames: {list(evil_bypassed)}")

        if errors:
            pytest.fail(" | ".join(errors))