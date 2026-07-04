# test_final_state.py

import os
import subprocess
import re

def test_cpp_fixed():
    cpp_path = "/home/user/polymath/src/integrate.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist"
    with open(cpp_path, "r") as f:
        content = f.read()

    # The fix should swap the 4.0 and 2.0 or change the condition
    # Original: (i % 2 == 0) ? 4.0 : 2.0;
    # Fixed: (i % 2 == 0) ? 2.0 : 4.0; or (i % 2 != 0) ? 4.0 : 2.0;

    # Let's just check that it produces the correct output by compiling it, 
    # but we can also do a basic check that the buggy line is gone or changed.
    assert "4.0 : 2.0" not in content or "i % 2 != 0" in content or "i % 2 == 1" in content, \
        "The bug in integrate.cpp does not appear to be fixed correctly."

def test_patch_exists():
    patch_path = "/home/user/polymath/simpson.patch"
    assert os.path.isfile(patch_path), f"{patch_path} was not created"
    with open(patch_path, "r") as f:
        content = f.read()
    assert "integrate.cpp" in content, "Patch file does not seem to modify integrate.cpp"
    assert "+" in content and "-" in content, "Patch file does not look like a valid diff"

def test_makefile_exists_and_targets():
    makefile_path = "/home/user/polymath/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} was not created"
    with open(makefile_path, "r") as f:
        content = f.read()

    # Check for targets
    assert re.search(r'^build:', content, re.MULTILINE), "Makefile is missing 'build' target"
    assert re.search(r'^test:', content, re.MULTILINE), "Makefile is missing 'test' target"
    assert re.search(r'^clean:', content, re.MULTILINE), "Makefile is missing 'clean' target"

def test_make_workflow():
    workdir = "/home/user/polymath"

    # Test clean
    subprocess.run(["make", "clean"], cwd=workdir, capture_output=True)
    assert not os.path.exists(os.path.join(workdir, "bin", "integrate")), "'make clean' did not remove the binary"

    # Test build
    res_build = subprocess.run(["make", "build"], cwd=workdir, capture_output=True)
    assert res_build.returncode == 0, f"'make build' failed: {res_build.stderr.decode()}"

    binary_path = os.path.join(workdir, "bin", "integrate")
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not created by 'make build'"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable"

    # Test binary execution
    res_bin = subprocess.run([binary_path, "0", "2", "100"], capture_output=True, text=True)
    assert res_bin.returncode == 0, "Binary execution failed"
    output = res_bin.stdout.strip()
    assert output == "4.00000", f"Expected binary output '4.00000', got '{output}'"

def test_make_test():
    workdir = "/home/user/polymath"
    res_test = subprocess.run(["make", "test"], cwd=workdir, capture_output=True, text=True)
    assert res_test.returncode == 0, f"'make test' failed. Output:\n{res_test.stdout}\n{res_test.stderr}"
    assert "pytest" in res_test.stdout or "pytest" in res_test.stderr, "'make test' doesn't seem to invoke pytest"