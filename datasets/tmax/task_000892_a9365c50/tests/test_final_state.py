# test_final_state.py

import os
import re
import subprocess
import pytest

def test_cwe_identification():
    cwe_file = "/home/user/cwe.txt"
    assert os.path.isfile(cwe_file), f"File {cwe_file} does not exist."

    with open(cwe_file, "r") as f:
        content = f.read().strip().upper()

    valid_cwes = ["CWE-120", "CWE-121", "CWE-119", "CWE-242"]
    found = any(cwe in content for cwe in valid_cwes)
    assert found, f"File {cwe_file} does not contain a valid CWE identifier for the vulnerability. Expected one of {valid_cwes}."

def test_exploit_crafting():
    exploit_script = "/home/user/exploit.py"
    target_binary = "/home/user/greeter"

    assert os.path.isfile(exploit_script), f"Exploit script {exploit_script} does not exist."
    assert os.path.isfile(target_binary), f"Target binary {target_binary} does not exist."

    try:
        p1 = subprocess.Popen(["python3", exploit_script], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([target_binary], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p1.stdout.close()
        stdout, stderr = p2.communicate(timeout=5)

        output = stdout.decode(errors='ignore')
        assert "POLICY_BYPASS_SUCCESS" in output, "The exploit did not successfully hijack execution to print POLICY_BYPASS_SUCCESS."
    except subprocess.TimeoutExpired:
        pytest.fail("The exploit execution timed out.")
    except Exception as e:
        pytest.fail(f"An error occurred while running the exploit: {e}")

def test_sshd_config_fixed():
    fixed_config = "/home/user/sshd_config.fixed"
    assert os.path.isfile(fixed_config), f"Hardened config file {fixed_config} does not exist."

    with open(fixed_config, "r") as f:
        lines = f.readlines()

    def check_directive(directive, expected_value):
        pattern = re.compile(rf"^\s*{directive}\s+{expected_value}\s*$", re.IGNORECASE)
        for line in lines:
            if pattern.match(line):
                return True
        return False

    assert check_directive("PermitRootLogin", "no"), "PermitRootLogin is not explicitly set to 'no' or is commented out."
    assert check_directive("PasswordAuthentication", "no"), "PasswordAuthentication is not explicitly set to 'no' or is commented out."
    assert check_directive("Protocol", "2"), "Protocol is not explicitly set to '2' or is commented out."

def test_policy_as_code_bad_config():
    policy_script = "/home/user/policy.py"
    bad_config = "/home/user/sshd_config"

    assert os.path.isfile(policy_script), f"Policy script {policy_script} does not exist."
    assert os.path.isfile(bad_config), f"Config file {bad_config} does not exist."

    result = subprocess.run(["python3", policy_script, bad_config], capture_output=True, text=True)

    assert result.returncode == 1, f"Policy script should exit with code 1 for insecure config, but exited with {result.returncode}."
    assert "FAIL" in result.stdout, "Policy script should print FAIL to stdout for insecure config."

def test_policy_as_code_good_config():
    policy_script = "/home/user/policy.py"
    good_config = "/home/user/sshd_config.fixed"

    assert os.path.isfile(policy_script), f"Policy script {policy_script} does not exist."
    assert os.path.isfile(good_config), f"Config file {good_config} does not exist."

    result = subprocess.run(["python3", policy_script, good_config], capture_output=True, text=True)

    assert result.returncode == 0, f"Policy script should exit with code 0 for hardened config, but exited with {result.returncode}."
    assert "PASS" in result.stdout, "Policy script should print PASS to stdout for hardened config."