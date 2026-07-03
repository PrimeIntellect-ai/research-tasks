# test_final_state.py

import os
import re
import stat
import pytest

def get_expected_interface():
    log_file = "/home/user/inventory_dump.log"
    sys_mock_dir = "/home/user/sys_mock"

    assert os.path.exists(log_file), f"{log_file} is missing."

    target_mac = None
    with open(log_file, "r") as f:
        for line in f:
            if "ROLE: storage_backend" in line:
                match = re.search(r"MAC:\s*([0-9a-fA-F:]+)", line)
                if match:
                    target_mac = match.group(1).lower()
                    break

    assert target_mac is not None, "Could not find storage_backend MAC in inventory_dump.log."

    target_iface = None
    for iface in os.listdir(sys_mock_dir):
        addr_file = os.path.join(sys_mock_dir, iface, "address")
        if os.path.isfile(addr_file):
            with open(addr_file, "r") as f:
                mac = f.read().strip().lower()
                if mac == target_mac:
                    target_iface = iface
                    break

    assert target_iface is not None, f"Could not find interface for MAC {target_mac} in {sys_mock_dir}."
    return target_iface

def test_build_routes_script_exists():
    allowed_extensions = ['.py', '.rb', '.pl']
    found = False
    for ext in allowed_extensions:
        if os.path.isfile(f"/home/user/build_routes{ext}"):
            found = True
            break
    assert found, "build_routes script (with .py, .rb, or .pl extension) is missing."

def test_apply_routes_sh():
    script_path = "/home/user/apply_routes.sh"
    assert os.path.isfile(script_path), f"{script_path} was not generated."

    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) >= 3, f"{script_path} does not contain enough lines."
    assert content[0] == "#!/bin/bash", f"First line of {script_path} is not #!/bin/bash."

    target_iface = get_expected_interface()

    # Check for ip route command
    route_cmd_pattern = rf"ip route add 10\.50\.0\.0/16 via 10\.50\.0\.1 dev {target_iface}"
    route_found = any(re.search(route_cmd_pattern, line) for line in content)
    assert route_found, f"Expected route command for {target_iface} not found in {script_path}."

    # Check for environment variable append command
    env_cmd_pattern = rf"echo\s+['\"]?(export\s+)?STORAGE_IFACE={target_iface}['\"]?\s+>>\s+/home/user/\.bash_profile"
    env_found = any(re.search(env_cmd_pattern, line) for line in content)
    assert env_found, f"Expected command to append STORAGE_IFACE={target_iface} to .bash_profile not found in {script_path}."