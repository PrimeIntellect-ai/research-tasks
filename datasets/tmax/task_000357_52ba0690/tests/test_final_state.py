# test_final_state.py
import os
import hashlib

def test_resolution_file():
    """Verify that resolution.txt contains the correct dependency resolution."""
    resolution_path = "/home/user/project/build/resolution.txt"
    assert os.path.exists(resolution_path), f"Resolution file missing at {resolution_path}"

    with open(resolution_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = ["core:1.0", "net:2.0", "ui:1.1"]

    for line in expected_lines:
        assert line in content, f"Expected '{line}' in resolution.txt, but it was missing."

    assert len(content) == 3, f"Expected exactly 3 lines in resolution.txt, got {len(content)}."

def test_binaries_exist():
    """Verify that the compiled binaries exist."""
    x86_path = "/home/user/project/build/app_x86"
    arm_path = "/home/user/project/build/app_arm"

    assert os.path.exists(x86_path), f"Binary missing at {x86_path}"
    assert os.path.exists(arm_path), f"Binary missing at {arm_path}"
    assert os.path.isfile(x86_path), f"{x86_path} is not a file"
    assert os.path.isfile(arm_path), f"{arm_path} is not a file"

def test_manifest_file():
    """Verify the manifest file contains correct hashes and parity."""
    manifest_path = "/home/user/project/build/manifest.txt"
    x86_path = "/home/user/project/build/app_x86"
    arm_path = "/home/user/project/build/app_arm"

    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        manifest_lines = f.read().strip().splitlines()

    manifest_dict = {}
    for line in manifest_lines:
        if ':' in line:
            k, v = line.split(':', 1)
            manifest_dict[k.strip()] = v.strip()

    assert "app_x86" in manifest_dict, "Manifest missing 'app_x86' entry."
    assert "app_arm" in manifest_dict, "Manifest missing 'app_arm' entry."
    assert "PARITY" in manifest_dict, "Manifest missing 'PARITY' entry."

    # Calculate expected hashes
    with open(x86_path, "rb") as f:
        x86_data = f.read()
    x86_hash = hashlib.sha256(x86_data).hexdigest()
    x86_raw = hashlib.sha256(x86_data).digest()

    with open(arm_path, "rb") as f:
        arm_data = f.read()
    arm_hash = hashlib.sha256(arm_data).hexdigest()
    arm_raw = hashlib.sha256(arm_data).digest()

    # Calculate parity
    parity = 0
    for b in x86_raw + arm_raw:
        parity ^= b
    expected_parity = f"{parity:02x}"

    assert manifest_dict["app_x86"] == x86_hash, f"Expected app_x86 hash {x86_hash}, got {manifest_dict['app_x86']}"
    assert manifest_dict["app_arm"] == arm_hash, f"Expected app_arm hash {arm_hash}, got {manifest_dict['app_arm']}"
    assert manifest_dict["PARITY"].lower() == expected_parity, f"Expected PARITY {expected_parity}, got {manifest_dict['PARITY']}"