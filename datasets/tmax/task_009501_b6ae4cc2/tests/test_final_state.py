# test_final_state.py

import os
import hashlib

def test_skipped_txt_contents():
    skipped_path = "/home/user/project/skipped.txt"
    assert os.path.isfile(skipped_path), f"{skipped_path} does not exist."

    with open(skipped_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_skipped = {"../escaped.txt", "/etc/fake_root.txt"}
    actual_skipped = set(lines)

    assert actual_skipped == expected_skipped, f"Expected skipped.txt to contain {expected_skipped}, but got {actual_skipped}"
    assert len(lines) == 2, f"Expected exactly 2 lines in skipped.txt, but got {len(lines)}"

def test_manifest_txt_contents():
    manifest_path = "/home/user/project/manifest.txt"
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist."

    # Recompute expected hashes based on the expected final state
    expected_files = {
        "app.log": b"unchanged_content",
        "config.json": b"v2_config",
        "feature.go": b"new_feature",
        "src/main.go": b"package main"
    }

    expected_manifest_lines = []
    for rel_path, content in expected_files.items():
        file_hash = hashlib.sha256(content).hexdigest()
        expected_manifest_lines.append(f"{file_hash} {rel_path}")

    expected_manifest_lines.sort()

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_manifest_lines, f"Manifest contents do not match expected. Expected:\n{expected_manifest_lines}\nGot:\n{actual_lines}"

def test_zip_slip_prevented():
    # Ensure the malicious files were not extracted outside the intended directory
    assert not os.path.exists("/home/user/escaped.txt"), "Zip Slip vulnerability triggered: /home/user/escaped.txt was extracted."
    assert not os.path.exists("/home/user/project/escaped.txt"), "Malicious file escaped.txt was extracted into the project directory."
    assert not os.path.exists("/etc/fake_root.txt"), "Zip Slip vulnerability triggered: /etc/fake_root.txt was extracted."

def test_project_files_updated():
    # Verify that the safe files were actually updated/created
    config_path = "/home/user/project/config.json"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        assert f.read() == "v2_config", "config.json was not updated correctly."

    feature_path = "/home/user/project/feature.go"
    assert os.path.isfile(feature_path), f"{feature_path} does not exist."
    with open(feature_path, "r") as f:
        assert f.read() == "new_feature", "feature.go was not extracted correctly."

    app_log_path = "/home/user/project/app.log"
    assert os.path.isfile(app_log_path), f"{app_log_path} does not exist."
    with open(app_log_path, "r") as f:
        assert f.read() == "unchanged_content", "app.log was modified unexpectedly."