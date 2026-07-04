# test_final_state.py

import os
import subprocess

def test_curation_log():
    log_path = "/home/user/curation.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "ACCEPTED: 1_base.tar",
        "REJECTED: 2_inc.tar",
        "ACCEPTED: 3_inc.tar",
        "REJECTED: 4_inc.tar"
    ]
    assert lines == expected, f"Log content mismatch. Expected {expected}, got {lines}"

def test_malicious_files_not_extracted():
    repo_path = "/home/user/repo"

    for root, _, files in os.walk(repo_path):
        for f in files:
            assert not f.startswith("app3"), f"Malicious archive 2_inc.tar was extracted! Found {f}"
            assert "evil.sh" not in f, f"Malicious file evil.sh was extracted into {root}!"
            assert "shadow_overwrite" not in f, f"Malicious file shadow_overwrite was extracted into {root}!"

def test_safe_files_extracted_and_renamed():
    repo_bin = "/home/user/repo/bin"
    assert os.path.isdir(repo_bin), f"Directory {repo_bin} does not exist. Safe archives were not extracted correctly."

    files = os.listdir(repo_bin)
    found_bases = set()

    for f in files:
        filepath = os.path.join(repo_bin, f)

        # Skip directories if any
        if not os.path.isfile(filepath):
            continue

        out = subprocess.check_output(["file", filepath]).decode()

        # Determine expected suffix based on `file` output
        expected_suffix = ""
        if "x86-64" in out:
            expected_suffix = "_x86_64"
        elif "aarch64" in out:
            expected_suffix = "_aarch64"
        elif "ARM" in out:
            expected_suffix = "_arm"
        elif "386" in out:
            expected_suffix = "_i386"

        assert expected_suffix != "", f"Could not determine expected architecture suffix for {f}. `file` output: {out}"
        assert f.endswith(expected_suffix), f"File '{f}' does not have the expected suffix '{expected_suffix}' for its architecture."

        base_name = f[:-len(expected_suffix)]
        found_bases.add(base_name)

    assert found_bases == {"app1", "app2", "app4"}, f"Expected extracted binaries app1, app2, app4. Found: {found_bases}"