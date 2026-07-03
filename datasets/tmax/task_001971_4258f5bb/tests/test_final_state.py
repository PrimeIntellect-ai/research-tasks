# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_binary_built():
    binary_path = "/app/fast-pcap-extract-1.2/pcap_extract"
    assert os.path.isfile(binary_path), f"Binary not found at {binary_path}. Makefile was not fixed or make was not run."
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_output_directory_permissions():
    out_dir = "/home/user/extracted_payloads"
    assert os.path.isdir(out_dir), f"Output directory {out_dir} does not exist. Did the tool run successfully?"

    # Check directory permissions (should be 0700)
    st = os.stat(out_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Output directory permissions are {oct(perms)}, expected 0o700."

def test_output_file_permissions():
    out_dir = "/home/user/extracted_payloads"
    assert os.path.isdir(out_dir), f"Output directory {out_dir} does not exist."

    # Check hashes.txt and other files
    hashes_file = os.path.join(out_dir, "hashes.txt")
    assert os.path.isfile(hashes_file), f"hashes.txt not found in {out_dir}"

    for filename in os.listdir(out_dir):
        filepath = os.path.join(out_dir, filename)
        if os.path.isfile(filepath):
            st = os.stat(filepath)
            perms = stat.S_IMODE(st.st_mode)
            assert perms == 0o600, f"File {filepath} has permissions {oct(perms)}, expected 0o600."

def test_vulnerability_remediation_source():
    writer_c = "/app/fast-pcap-extract-1.2/writer.c"
    assert os.path.isfile(writer_c), f"Source file {writer_c} missing."

    with open(writer_c, "r") as f:
        content = f.read()

    assert "0666" not in content, "Insecure file permissions (0666) still found in writer.c"
    assert "0777" not in content, "Insecure directory permissions (0777) still found in writer.c"

def test_performance_optimization_source():
    matcher_c = "/app/fast-pcap-extract-1.2/matcher.c"
    assert os.path.isfile(matcher_c), f"Source file {matcher_c} missing."

    with open(matcher_c, "r") as f:
        content = f.read()

    # Check if memmem or a more optimized approach is used
    # A naive check: if the original naive loop is gone or memmem is present
    has_memmem = "memmem" in content
    has_kmp = "kmp" in content.lower()
    has_opt = has_memmem or has_kmp or ("O3" in open("/app/fast-pcap-extract-1.2/Makefile").read())

    # We won't strictly fail just on source, but it's a good indicator.
    # The actual speedup metric is evaluated by the verifier script.

def test_verifier_script_if_present():
    verifier_script = "/opt/verifier/evaluate_speedup.py"
    if os.path.isfile(verifier_script):
        result = subprocess.run(["python3", verifier_script], capture_output=True, text=True)
        assert result.returncode == 0, f"Verifier script failed:\n{result.stdout}\n{result.stderr}"