# test_final_state.py

import os
import stat
import subprocess

def get_expected_iface():
    with open('/proc/net/route', 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) > 1 and parts[1] == "00000000":
                return parts[0]
    return ""

def test_gateway_finder_executable():
    bin_path = "/home/user/bin/gateway_finder"
    assert os.path.isfile(bin_path), f"Executable {bin_path} does not exist."
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{bin_path} is not executable."

def test_run_finder_script():
    script_path = "/home/user/run_finder.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_bash_profile():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"{profile_path} does not exist."
    with open(profile_path, 'r') as f:
        content = f.read()
    assert "export DEFAULT_GW_CHECK=1" in content, f"{profile_path} does not contain 'export DEFAULT_GW_CHECK=1'."

def test_iface_log_output():
    log_path = "/home/user/output/iface.log"
    assert os.path.isfile(log_path), f"Output file {log_path} does not exist. Did you run the wrapper script?"

    expected_iface = get_expected_iface()
    with open(log_path, 'r') as f:
        actual_iface = f.read().strip()

    assert actual_iface == expected_iface, f"Expected interface '{expected_iface}', but got '{actual_iface}' in {log_path}."

def test_gateway_finder_functionality():
    bin_path = "/home/user/bin/gateway_finder"
    test_log_path = "/home/user/test_iface.log"

    # Remove the file if it exists from previous runs
    if os.path.exists(test_log_path):
        os.remove(test_log_path)

    env = os.environ.copy()
    env["GW_OUT_FILE"] = test_log_path

    result = subprocess.run([bin_path], env=env, capture_output=True)
    assert result.returncode == 0, f"{bin_path} did not exit cleanly."

    assert os.path.isfile(test_log_path), f"{bin_path} did not create the output file specified by GW_OUT_FILE."

    expected_iface = get_expected_iface()
    with open(test_log_path, 'r') as f:
        actual_iface = f.read().strip()

    assert actual_iface == expected_iface, f"Binary produced '{actual_iface}' instead of '{expected_iface}'."