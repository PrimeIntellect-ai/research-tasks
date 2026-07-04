# test_final_state.py

import os
import re

def test_build_system_script_exists_and_executable():
    script_path = "/home/user/build_system.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_sec_tool_executable_exists():
    bin_path = "/home/user/bin/sec_tool"
    assert os.path.isfile(bin_path), f"{bin_path} does not exist"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable"

def test_build_output_log_contents():
    log_path = "/home/user/build_output.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "Entropy: 3.6622" in content, "Expected 'Entropy: 3.6622' in build_output.log"
    assert "WS: Upgrade Request" in content, "Expected 'WS: Upgrade Request' in build_output.log"
    assert "REST: Fallback Request" in content, "Expected 'REST: Fallback Request' in build_output.log"

def test_build_system_script_resolves_circular_dependency():
    script_path = "/home/user/build_system.sh"
    with open(script_path, 'r') as f:
        content = f.read()

    # Check for GNU linker group flags
    assert "--start-group" in content and "--end-group" in content, (
        "The build script does not seem to use GNU linker group flags "
        "(--start-group and --end-group) to resolve circular dependencies."
    )

    # Ensure both libraries are mentioned in the script
    assert "libws.a" in content, "libws.a not found in the build script"
    assert "librest.a" in content, "librest.a not found in the build script"