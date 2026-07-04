# test_final_state.py
import os
import re
import subprocess

def test_tokens_txt():
    assert os.path.isfile("/home/user/tokens.txt"), "/home/user/tokens.txt does not exist."

    with open("/home/user/raw_corpus.txt", "r") as f:
        raw_text = f.read()

    # Recompute expected tokens
    cleaned = re.sub(r'[^a-zA-Z0-9]', ' ', raw_text.lower())
    expected_tokens = [t for t in cleaned.split(' ') if t]

    with open("/home/user/tokens.txt", "r") as f:
        actual_tokens = [line.strip() for line in f if line.strip()]

    assert actual_tokens == expected_tokens, "/home/user/tokens.txt content does not match the expected tokenized output."

def test_bootstrap_script_exists_and_executable():
    script_path = "/home/user/bootstrap.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_samples_and_checksums():
    # Verify the sample files exist
    samples = {
        42: "/home/user/sample_42.txt",
        123: "/home/user/sample_123.txt",
        999: "/home/user/sample_999.txt"
    }

    for seed, path in samples.items():
        assert os.path.isfile(path), f"Sample file {path} does not exist."
        with open(path, "r") as f:
            lines = f.readlines()
        assert len(lines) == 1000, f"Sample file {path} should have exactly 1000 lines."

    # Verify checksums.txt exists
    checksums_path = "/home/user/checksums.txt"
    assert os.path.isfile(checksums_path), f"{checksums_path} does not exist."

    # Recompute expected checksums using awk
    expected_checksums = {}
    tokens_path = "/home/user/tokens.txt"

    for seed, path in samples.items():
        awk_cmd = f"""awk -v n=1000 -v s={seed} 'BEGIN {{ srand(s) }} {{ lines[NR]=$0 }} END {{ for(i=1; i<=n; i++) {{ idx=int(rand()*NR)+1; print lines[idx] }} }}' {tokens_path}"""
        expected_output = subprocess.check_output(awk_cmd, shell=True)

        # Calculate sha256
        import hashlib
        h = hashlib.sha256(expected_output).hexdigest()
        expected_checksums[path] = h

        # Also check if the actual file matches the expected output
        with open(path, "rb") as f:
            actual_output = f.read()
            assert actual_output == expected_output, f"Content of {path} does not match the expected bootstrap sample for seed {seed}."

    # Verify checksums.txt content
    with open(checksums_path, "r") as f:
        checksums_content = f.read()

    for path, expected_hash in expected_checksums.items():
        assert expected_hash in checksums_content, f"Expected hash {expected_hash} for {path} not found in {checksums_path}."
        assert f"{expected_hash}  {path}" in checksums_content or f"{expected_hash} {path}" in checksums_content, f"Expected correctly formatted checksum line for {path} in {checksums_path}."