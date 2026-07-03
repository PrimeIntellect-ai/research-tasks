# test_final_state.py

import os
import stat
import subprocess
import tempfile
import json
import pytest

def test_build_runner_patched():
    script_path = "/home/user/pipeline/build_runner.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist"

    with open(script_path, "r") as f:
        content = f.read()

    assert "eval" not in content, "Vulnerability not patched: 'eval' is still present in build_runner.sh"
    assert "make" in content, "Script does not seem to call 'make' anymore. Functionality might be broken."

def test_audit_report():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    cwe = data.get("build_runner_cwe")
    assert cwe in ["CWE-78", "CWE-77"], f"Expected CWE-78 or CWE-77 for build_runner_cwe, got {cwe}"

    secret = data.get("validator_secret")
    assert secret == "AUTH_KEY_9921_DEV", f"Incorrect validator secret found: {secret}"

def test_enforce_policy_script():
    script_path = "/home/user/enforce_policy.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    log_file = "/home/user/fixed_files.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        f_normal = os.path.join(temp_dir, "normal.txt")
        f_suid = os.path.join(temp_dir, "suid.txt")
        f_sgid = os.path.join(temp_dir, "sgid.txt")
        f_ww = os.path.join(temp_dir, "ww.txt")
        f_all = os.path.join(temp_dir, "all.txt")

        for f in [f_normal, f_suid, f_sgid, f_ww, f_all]:
            with open(f, "w") as fp:
                fp.write("test data")

        # Set specific permissions
        os.chmod(f_normal, 0o644)
        os.chmod(f_suid, 0o4755)
        os.chmod(f_sgid, 0o2755)
        os.chmod(f_ww, 0o666)
        os.chmod(f_all, 0o6777)

        # Run the policy enforcement script
        result = subprocess.run([script_path, temp_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"enforce_policy.sh failed with output: {result.stderr}"

        # Verify permissions were removed
        assert not (os.stat(f_suid).st_mode & stat.S_ISUID), "SUID bit was not removed"
        assert not (os.stat(f_sgid).st_mode & stat.S_ISGID), "SGID bit was not removed"
        assert not (os.stat(f_ww).st_mode & stat.S_IWOTH), "World-writable bit was not removed"

        st_all = os.stat(f_all).st_mode
        assert not (st_all & stat.S_ISUID), "SUID bit was not removed from multi-bad file"
        assert not (st_all & stat.S_ISGID), "SGID bit was not removed from multi-bad file"
        assert not (st_all & stat.S_IWOTH), "World-writable bit was not removed from multi-bad file"

        # Verify normal file was untouched
        assert stat.S_IMODE(os.stat(f_normal).st_mode) == 0o644, "Normal file permissions were incorrectly altered"

        # Verify the log file
        assert os.path.isfile(log_file), f"Log file {log_file} was not created"
        with open(log_file, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        expected_modified = sorted([f_suid, f_sgid, f_ww, f_all])
        assert lines == expected_modified, f"Log file contents do not match expected sorted paths. Expected {expected_modified}, got {lines}"