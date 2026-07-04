# test_final_state.py

import os
import json
import stat
import pytest

def test_allocation_log_exists_and_valid():
    log_path = "/home/user/allocation.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        try:
            allocation = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} is not valid JSON.")

    expected_files = {"a.c", "b.c", "c.py", "d.c", "e.c", "f.py"}
    assert set(allocation.keys()) == expected_files, f"Allocation log keys do not match expected files: {expected_files}"

    bins = set(allocation.values())
    assert len(bins) == 2, f"Expected exactly 2 bins to minimize bins, found {len(bins)}: {bins}"

def test_conflict_constraint():
    log_path = "/home/user/allocation.log"
    if not os.path.isfile(log_path):
        pytest.skip("Allocation log missing")

    with open(log_path, "r") as f:
        allocation = json.load(f)

    bin_a = allocation.get("a.c")
    bin_b = allocation.get("b.c")

    assert bin_a is not None and bin_b is not None, "Missing allocation for a.c or b.c"
    assert bin_a != bin_b, "Conflict constraint violated: a.c (x86) and b.c (arm) are in the same bin."

def test_build_scripts_and_capacity():
    log_path = "/home/user/allocation.log"
    if not os.path.isfile(log_path):
        pytest.skip("Allocation log missing")

    with open(log_path, "r") as f:
        allocation = json.load(f)

    organized_dir = "/home/user/organized"
    assert os.path.isdir(organized_dir), f"{organized_dir} does not exist."

    bins = set(allocation.values())

    for bin_name in bins:
        bin_dir = os.path.join(organized_dir, bin_name)
        assert os.path.isdir(bin_dir), f"Bin directory {bin_dir} does not exist."

        # Check capacity
        total_size = 0
        bin_files = [f for f, b in allocation.items() if b == bin_name]
        has_x86 = False
        has_arm = False

        for filename in bin_files:
            file_path = os.path.join(bin_dir, filename)
            assert os.path.isfile(file_path), f"File {filename} missing in {bin_dir}"
            total_size += os.path.getsize(file_path)

            with open(file_path, "r", encoding="utf-8") as file_obj:
                content = file_obj.read()
                if "ARCH: x86" in content:
                    has_x86 = True
                if "ARCH: arm" in content:
                    has_arm = True

        assert total_size <= 100, f"Bin {bin_name} exceeds 100 bytes: {total_size} bytes."
        assert not (has_x86 and has_arm), f"Bin {bin_name} contains both x86 and arm files."

        # Check build.sh
        build_script_path = os.path.join(bin_dir, "build.sh")
        assert os.path.isfile(build_script_path), f"build.sh missing in {bin_dir}"

        st = os.stat(build_script_path)
        assert st.st_mode & stat.S_IXUSR, f"build.sh in {bin_dir} is not executable."

        with open(build_script_path, "r", encoding="utf-8") as build_obj:
            build_content = build_obj.read().strip()

        if has_x86:
            assert "gcc -m64 -c *.c" in build_content, f"build.sh in {bin_dir} missing x86 command."
        elif has_arm:
            assert "aarch64-linux-gnu-gcc -c *.c" in build_content, f"build.sh in {bin_dir} missing arm command."
        else:
            assert "python3 -m py_compile *.*" in build_content, f"build.sh in {bin_dir} missing any command."