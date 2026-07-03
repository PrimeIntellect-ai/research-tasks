# test_final_state.py

import os
import subprocess
import pytest

def test_binary_exists_and_executable():
    binary_path = "/home/user/project/bin/server"
    assert os.path.isfile(binary_path), f"Executable {binary_path} not found."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

def test_binary_linking_rpath():
    binary_path = "/home/user/project/bin/server"
    # Run ldd to check if libsolver.so is found without LD_LIBRARY_PATH
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        del env["LD_LIBRARY_PATH"]

    result = subprocess.run(
        ["ldd", binary_path],
        capture_output=True,
        text=True,
        env=env
    )
    assert result.returncode == 0, f"ldd failed on {binary_path}"

    # Check that libsolver.so is resolved (does not say "not found")
    found_libsolver = False
    for line in result.stdout.splitlines():
        if "libsolver.so" in line:
            found_libsolver = True
            assert "not found" not in line, "libsolver.so is 'not found' by ldd. Rpath/Runpath is likely missing or incorrect."
            break

    assert found_libsolver, "libsolver.so is not linked in the final binary."

def test_hub_go_concurrency_fixes():
    hub_go_path = "/home/user/project/src/hub.go"
    assert os.path.isfile(hub_go_path), f"Source file {hub_go_path} is missing."

    with open(hub_go_path, 'r') as f:
        content = f.read()

    assert "sync" in content, "The 'sync' package is not imported in hub.go."
    assert "Mutex" in content, "No Mutex or RWMutex found in hub.go."
    assert "Lock()" in content, "Mutex Lock() not found in hub.go."
    assert "Unlock()" in content, "Mutex Unlock() not found in hub.go."

def test_main_go_cgo_directives():
    main_go_path = "/home/user/project/src/main.go"
    assert os.path.isfile(main_go_path), f"Source file {main_go_path} is missing."

    with open(main_go_path, 'r') as f:
        content = f.read()

    # Check for library path flag
    assert "-L" in content or "LDFLAGS" in content, "LDFLAGS missing in main.go cgo directives."

    # Check for rpath or absolute path link
    has_rpath = "-Wl,-rpath" in content or "-Wl,-R" in content
    has_abs_path = "/home/user/project/lib" in content
    assert has_rpath or has_abs_path, "No rpath directive or absolute library path found in main.go LDFLAGS."