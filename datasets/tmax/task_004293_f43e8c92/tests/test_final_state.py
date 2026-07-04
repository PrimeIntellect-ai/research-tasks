# test_final_state.py
import os

def test_deployment_sequence_file():
    output_file = "/home/user/deployment_sequence.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "ABCE", f"Expected output sequence 'ABCE', but got '{content}'"

def test_makefile_fixed():
    makefile_path = "/home/user/release/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    # Check that it links vm.o in the release_vm target
    assert "vm.o" in content.split("release_vm:")[1], "Makefile still does not link vm.o correctly."

def test_vm_c_fixed():
    vm_c_path = "/home/user/release/vm.c"
    assert os.path.isfile(vm_c_path), "vm.c is missing."

    with open(vm_c_path, "r") as f:
        content = f.read()

    # The bug was `if (state[(int)arg2] == 1) {`
    # It should be fixed to check for 0 or false.
    assert "state[(int)arg2] == 1" not in content, "vm.c still contains the logical bug checking for == 1 in the REQ instruction."

def test_executable_exists():
    exe_path = "/home/user/release/release_vm"
    assert os.path.isfile(exe_path), "release_vm executable is missing. Did you run make?"
    assert os.access(exe_path, os.X_OK), "release_vm is not executable."