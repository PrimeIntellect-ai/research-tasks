# test_final_state.py
import os
import json
import subprocess

def test_output_json_correct():
    output_path = "/home/user/pr-review/output.json"
    assert os.path.isfile(output_path), f"Expected {output_path} to exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_path} is not valid JSON."

    expected = [9, 17, 27, 47, 107, 207]
    assert data == expected, f"Expected output.json to contain {expected}, but got {data}."

def test_libvm_so_built():
    so_path = "/home/user/pr-review/libvm.so"
    assert os.path.isfile(so_path), f"Expected {so_path} to be built."

    # Check if it's an ELF file
    with open(so_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{so_path} is not a valid ELF binary."

def test_pytest_passes():
    test_path = "/home/user/pr-review/test_vm.py"
    assert os.path.isfile(test_path), f"Expected {test_path} to exist."

    result = subprocess.run(
        ["pytest", test_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_path} failed:\n{result.stdout}\n{result.stderr}"

def test_vm_c_fixed():
    vm_c_path = "/home/user/pr-review/vm.c"
    assert os.path.isfile(vm_c_path), f"Expected {vm_c_path} to exist."

    with open(vm_c_path, "r") as f:
        content = f.read()

    # The bug was in the ADD block: stack[sp++] = b - a;
    # It should be stack[sp++] = b + a;
    # We'll just verify the tests pass, but we can also check that the subtraction is gone from the ADD block.
    # A simple string check might be brittle, so we rely on the integration test (output.json) and pytest.
    # But just to be sure, we can check that `b + a` is present.
    assert "b + a" in content, f"Expected to find 'b + a' in {vm_c_path} for the ADD instruction fix."