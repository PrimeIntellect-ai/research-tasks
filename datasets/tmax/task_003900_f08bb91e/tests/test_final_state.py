# test_final_state.py
import os
import subprocess
import glob

def test_protein_classifier_exists():
    script_path = "/home/user/protein_classifier.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist. The agent failed to create the required file."

def test_clean_corpus_accepted():
    script_path = "/home/user/protein_classifier.py"
    clean_dir = "/app/corpus/clean"

    clean_files = glob.glob(os.path.join(clean_dir, "*.pdb"))
    if not clean_files:
        # Fallback if extensions differ or no extension
        clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}"

def test_evil_corpus_rejected():
    script_path = "/home/user/protein_classifier.py"
    evil_dir = "/app/corpus/evil"

    evil_files = glob.glob(os.path.join(evil_dir, "*.pdb"))
    if not evil_files:
        evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}"