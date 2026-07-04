# test_final_state.py
import os
import glob
import subprocess

def test_detector_exists():
    """Ensure the detector script was created at the correct path."""
    assert os.path.isfile("/home/user/detector.py"), "/home/user/detector.py does not exist."

def test_adversarial_corpus():
    """
    Iterate over the evil and clean corpora.
    Assert that the script prints 'EVIL' for malicious files and 'CLEAN' for benign ones.
    """
    detector_path = "/home/user/detector.py"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.req"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.req"))

    assert len(evil_files) > 0, f"No files found in evil corpus path: {evil_dir}"
    assert len(clean_files) > 0, f"No files found in clean corpus path: {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    # Check evil corpus
    for req_file in evil_files:
        result = subprocess.run(
            ["python3", detector_path, req_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "EVIL":
            evil_bypassed.append(os.path.basename(req_file))

    # Check clean corpus
    for req_file in clean_files:
        result = subprocess.run(
            ["python3", detector_path, req_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_modified.append(os.path.basename(req_file))

    # Compile failure messages
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus verification failed:\n" + "\n".join(errors)

def test_crypt_auth_lib_fixed():
    """Ensure the bug in the vendored package was fixed."""
    decryptor_path = "/app/crypt_auth_lib-2.1/crypt_auth_lib/decryptor.py"
    assert os.path.isfile(decryptor_path), f"{decryptor_path} is missing."

    with open(decryptor_path, "r") as f:
        content = f.read()

    assert "data[:16]" in content, "The IV extraction bug in crypt_auth_lib/decryptor.py was not fixed (expected 'data[:16]')."