# test_final_state.py

import os
import subprocess
import pytest

def test_rust_project_execution_and_output():
    automator_dir = "/home/user/automator"
    spec_file = "/home/user/deploy_spec.txt"
    vm_state_file = "/home/user/vm_state.conf"
    route_file = "/home/user/route-eth0.conf"

    # Ensure the Rust project directory exists
    assert os.path.isdir(automator_dir), f"Rust project directory missing: {automator_dir}"

    # Read the expected values from the spec file
    assert os.path.isfile(spec_file), f"Spec file missing: {spec_file}"
    with open(spec_file, "r") as f:
        spec_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(spec_lines) >= 4, "deploy_spec.txt does not have enough lines."
    tz, loc, ip, gw = spec_lines[:4]

    # Clean up previous state files if they exist to ensure the Rust program creates them
    if os.path.exists(vm_state_file):
        os.remove(vm_state_file)
    if os.path.exists(route_file):
        os.remove(route_file)

    # Run the Rust program
    try:
        result = subprocess.run(
            ["cargo", "run"],
            cwd=automator_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"'cargo run' failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    except FileNotFoundError:
        pytest.fail("Cargo is not installed or not found in PATH.")
    except subprocess.TimeoutExpired:
        pytest.fail("The Rust program timed out. Ensure it correctly interacts with the mock script and flushes I/O.")

    # Check vm_state.conf
    assert os.path.isfile(vm_state_file), f"The mock script did not create {vm_state_file}. The Rust program may not have completed the interaction successfully."
    with open(vm_state_file, "r") as f:
        vm_state_content = f.read()

    assert f"TZ={tz}" in vm_state_content, f"Expected TZ={tz} in {vm_state_file}"
    assert f"LOCALE={loc}" in vm_state_content, f"Expected LOCALE={loc} in {vm_state_file}"
    assert f"IP={ip}" in vm_state_content, f"Expected IP={ip} in {vm_state_file}"
    assert f"GW={gw}" in vm_state_content, f"Expected GW={gw} in {vm_state_file}"

    # Check route-eth0.conf
    assert os.path.isfile(route_file), f"The Rust program did not create {route_file}."
    with open(route_file, "r") as f:
        route_content = f.read().strip()

    expected_route = f"default via {gw} dev eth0"
    assert route_content == expected_route, f"Content of {route_file} is incorrect. Expected: '{expected_route}', but got: '{route_content}'"