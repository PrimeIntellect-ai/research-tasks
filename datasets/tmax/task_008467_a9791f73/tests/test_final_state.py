# test_final_state.py

import os
import re
import stat
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was initialized."""
    cargo_toml = "/home/user/finops_calc/Cargo.toml"
    main_rs = "/home/user/finops_calc/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Missing Rust project file: {cargo_toml}. Did you run 'cargo init'?"
    assert os.path.isfile(main_rs), f"Missing Rust source file: {main_rs}."

def test_network_storage_cost_calculation():
    """Verify the calculated storage cost from the fstab file."""
    fstab_path = "/home/user/cloud_fstab"
    output_path = "/home/user/network_storage_cost.txt"

    assert os.path.isfile(fstab_path), f"Missing required file: {fstab_path}"
    assert os.path.isfile(output_path), f"Missing output file: {output_path}. The Rust program must create this."

    # Recompute expected cost
    expected_cost = 0
    with open(fstab_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                fs_type = parts[2]
                if fs_type == "nfs":
                    expected_cost += 120
                elif fs_type == "cifs":
                    expected_cost += 85

    with open(output_path, 'r') as f:
        actual_cost_str = f.read().strip()

    assert actual_cost_str.isdigit(), f"Output file {output_path} must contain a plain integer."
    assert int(actual_cost_str) == expected_cost, f"Calculated cost {actual_cost_str} does not match expected cost {expected_cost}."

def test_run_billing_vm_script():
    """Verify the run_billing_vm.sh script exists, is executable, and contains required flags."""
    script_path = "/home/user/run_billing_vm.sh"

    assert os.path.isfile(script_path), f"Missing script file: {script_path}"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "qemu-system-x86_64" in content, "Script is missing 'qemu-system-x86_64'."
    assert "-m 128" in content, "Script is missing RAM allocation '-m 128'."
    assert "-kernel /home/user/bzImage" in content, "Script is missing kernel configuration '-kernel /home/user/bzImage'."
    assert "-vnc :2" in content, "Script is missing VNC configuration '-vnc :2'."
    assert "-append" in content, "Script is missing '-append' flag."
    assert "TZ=Europe/London" in content, "Script is missing 'TZ=Europe/London' in the append string."

    # Check if it runs in background
    assert re.search(r'(-daemonize|&)', content), "Script does not appear to run the VM in the background (missing -daemonize or &)."