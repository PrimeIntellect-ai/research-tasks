# test_final_state.py

import os
import subprocess

def test_patch_applied():
    """Check that the patch was applied by verifying math_ops.c exists."""
    assert os.path.exists("/home/user/rpn_calc/math_ops.c"), "math_ops.c does not exist. The patch was not applied."

def test_makefile_fixed():
    """Check that Makefile was fixed to link math_ops.o."""
    assert os.path.exists("/home/user/rpn_calc/Makefile"), "Makefile is missing."
    with open("/home/user/rpn_calc/Makefile", "r") as f:
        lines = f.readlines()

    linked_correctly = False
    for i, line in enumerate(lines):
        if line.startswith("calc:"):
            # Check the next line (the recipe) to see if math_ops.o is included
            if i + 1 < len(lines) and "math_ops.o" in lines[i+1]:
                linked_correctly = True
                break

    assert linked_correctly, "Makefile does not correctly link math_ops.o in the 'calc' target."

def test_executable_exists():
    """Check that the calc executable exists and is executable."""
    exe_path = "/home/user/rpn_calc/calc"
    assert os.path.isfile(exe_path), "The compiled 'calc' executable does not exist."
    assert os.access(exe_path, os.X_OK), "The 'calc' file is not executable."

def test_executable_behavior():
    """Check that the logic error in math_ops.c was fixed by testing the executable."""
    exe_path = "/home/user/rpn_calc/calc"
    if not os.path.isfile(exe_path) or not os.access(exe_path, os.X_OK):
        return # Skip if executable is missing, previous test will fail

    # Test 6! = 720 to ensure the logic was fixed correctly
    result = subprocess.run([exe_path], input=b"6 ! P\n", capture_output=True)
    output = result.stdout.decode('utf-8').strip()
    assert output == "720", f"The compiled calculator produced incorrect output for 6!: expected '720', got '{output}'. The logical error in math_ops.c may not be fixed."

def test_calc_output():
    """Check that calc_out.txt contains the correct output for 5!."""
    out_file = "/home/user/calc_out.txt"
    assert os.path.exists(out_file), f"{out_file} does not exist."

    with open(out_file, "r") as f:
        content = f.read().strip()

    assert content == "120", f"Expected {out_file} to contain '120', but got '{content}'."