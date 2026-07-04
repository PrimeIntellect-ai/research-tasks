# test_final_state.py

import os
import subprocess
import pytest

def fletcher16(data):
    sum1 = 0
    sum2 = 0
    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1

def test_binaries_exist():
    """Check if the raw binaries were generated properly."""
    app_bin = "/home/user/firmware/app.bin"
    boot_bin = "/home/user/firmware/boot.bin"

    assert os.path.isfile(app_bin), f"{app_bin} is missing. Did you compile and run objcopy?"
    assert os.path.getsize(app_bin) > 0, f"{app_bin} is empty."

    assert os.path.isfile(boot_bin), f"{boot_bin} is missing. Did you compile and run objcopy?"
    assert os.path.getsize(boot_bin) > 0, f"{boot_bin} is empty."

def test_verify_program_exists():
    """Check if verify.c and the compiled verify executable exist."""
    verify_c = "/home/user/verify.c"
    verify_bin = "/home/user/verify"

    assert os.path.isfile(verify_c), f"{verify_c} is missing."
    assert os.path.isfile(verify_bin), f"{verify_bin} is missing."
    assert os.access(verify_bin, os.X_OK), f"{verify_bin} is not executable."

def test_manifest_v2_contents():
    """Check if manifest_v2.txt contains the correct checksums."""
    manifest = "/home/user/manifest_v2.txt"
    assert os.path.isfile(manifest), f"{manifest} is missing."

    app_bin = "/home/user/firmware/app.bin"
    boot_bin = "/home/user/firmware/boot.bin"

    with open(app_bin, "rb") as f:
        app_data = f.read()
    with open(boot_bin, "rb") as f:
        boot_data = f.read()

    expected_app_csum = f"{fletcher16(app_data):04X}"
    expected_boot_csum = f"{fletcher16(boot_data):04X}"

    expected_lines = [
        f"app.bin: {expected_app_csum}",
        f"boot.bin: {expected_boot_csum}"
    ]

    with open(manifest, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().splitlines()]

    assert actual_lines == expected_lines, f"Contents of {manifest} do not match expected checksums."

def test_release_diff_patch():
    """Check if the release diff patch is a valid unified diff."""
    patch_file = "/home/user/release_diff.patch"
    assert os.path.isfile(patch_file), f"{patch_file} is missing."

    with open(patch_file, "r") as f:
        patch_content = f.read()

    assert "---" in patch_content and "+++" in patch_content, "Patch file does not look like a unified diff."
    assert "-app.bin: 0000" in patch_content, "Patch file does not contain the expected removal of the old app.bin checksum."
    assert "+app.bin:" in patch_content, "Patch file does not contain the addition of the new app.bin checksum."