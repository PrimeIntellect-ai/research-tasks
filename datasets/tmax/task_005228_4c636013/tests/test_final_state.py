# test_final_state.py

import os
import json
import subprocess
import shutil
import tempfile
import pytest

def test_storage_setup():
    img_path = "/home/user/capacity_data.img"
    mnt_path = "/home/user/mnt/capacity"
    fstab_path = "/home/user/fstab_mock"

    # Check image file
    assert os.path.isfile(img_path), f"Image file not found at {img_path}"

    # Check if it's ext4
    file_output = subprocess.check_output(["file", img_path]).decode("utf-8")
    assert "ext4 filesystem" in file_output.lower(), f"Image is not an ext4 filesystem: {file_output}"

    # Check if mounted
    mount_output = subprocess.check_output(["mount"]).decode("utf-8")
    assert mnt_path in mount_output, f"Mount point {mnt_path} is not mounted"

    # Check fstab_mock
    assert os.path.isfile(fstab_path), f"fstab_mock not found at {fstab_path}"
    with open(fstab_path, "r") as f:
        fstab_content = f.read()

    found_fstab_entry = False
    for line in fstab_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 4:
            if parts[0] == img_path and parts[1] == mnt_path and parts[2] == "ext4":
                opts = parts[3].split(",")
                if "noexec" in opts and "nodev" in opts:
                    found_fstab_entry = True
                    break

    assert found_fstab_entry, f"Correct fstab entry not found in {fstab_path}"

def test_physical_access_analysis():
    json_path = "/home/user/mnt/capacity/access_counts.json"
    assert os.path.isfile(json_path), f"JSON output not found at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} contains invalid JSON")

    assert "door_open_events" in data, f"'door_open_events' key missing in {json_path}"
    assert data["door_open_events"] == 4, f"Expected 4 door_open_events, got {data['door_open_events']}"

def test_resource_log_sanitization():
    script_path = "/home/user/sanitize_logs.py"
    assert os.path.isfile(script_path), f"Sanitizer script not found at {script_path}"

    clean_corpus = "/app/corpora/logs/clean/"
    evil_corpus = "/app/corpora/logs/evil/"

    with tempfile.TemporaryDirectory() as test_out_dir:
        # Run on clean corpus
        subprocess.run(["python3", script_path, "--input", clean_corpus, "--output", test_out_dir], check=True)

        clean_files = os.listdir(clean_corpus)
        out_files = os.listdir(test_out_dir)

        missing_clean = set(clean_files) - set(out_files)
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_files)} clean files were incorrectly rejected: {missing_clean}"

        # Clear output dir
        for f in out_files:
            os.remove(os.path.join(test_out_dir, f))

        # Run on evil corpus
        subprocess.run(["python3", script_path, "--input", evil_corpus, "--output", test_out_dir], check=True)

        evil_files = os.listdir(evil_corpus)
        out_files = os.listdir(test_out_dir)

        assert not out_files, f"{len(out_files)} of {len(evil_files)} evil files bypassed sanitization: {out_files}"