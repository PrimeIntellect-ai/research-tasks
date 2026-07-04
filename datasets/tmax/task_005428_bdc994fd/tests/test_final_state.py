# test_final_state.py

import os
import pytest

def test_malicious_log():
    """Verify that malicious paths were correctly logged to malicious.log."""
    log_path = "/home/user/malicious.log"
    assert os.path.exists(log_path), f"Missing file: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "../malicious_script.sh",
        "/etc/fake_shadow"
    ]

    assert set(lines) == set(expected_lines), f"Contents of {log_path} do not match expected. Got: {lines}"

def test_extrusion_total():
    """Verify that the total extrusion calculation is correct."""
    total_path = "/home/user/extrusion_total.txt"
    assert os.path.exists(total_path), f"Missing file: {total_path}"

    with open(total_path, "r") as f:
        content = f.read().strip()

    try:
        total = float(content)
    except ValueError:
        pytest.fail(f"Could not parse extrusion total as a float. Got: {content}")

    assert abs(total - 4.75) < 1e-6, f"Extrusion total is incorrect. Expected 4.75, got {total}"

def test_extracted_files():
    """Verify that safe files were correctly extracted to the extracted directory."""
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"Missing directory: {extracted_dir}"
    assert os.path.isdir(extracted_dir), f"Not a directory: {extracted_dir}"

    expected_files = {
        "normal1.gcode": b"G1 X10 Y10 E2.5\nG1 X20 E1.5\nM104 S200\n",
        "nested/dir/safe.gcode": b"G28\nG1 Z1.0 E0.5\nG1 X0 Y0 E0.25\n",
        "metadata.txt": b"Experiment 42 - Standard PLA",
    }

    for rel_path, expected_content in expected_files.items():
        abs_path = os.path.join(extracted_dir, rel_path)
        assert os.path.exists(abs_path), f"Missing extracted file: {abs_path}"
        assert os.path.isfile(abs_path), f"Not a file: {abs_path}"

        with open(abs_path, "rb") as f:
            content = f.read()

        assert content == expected_content, f"Content mismatch for {abs_path}."

def test_malicious_files_not_extracted():
    """Verify that malicious files were NOT extracted."""
    extracted_dir = "/home/user/extracted"

    # Check that they didn't get extracted relative to the extracted dir
    malicious_rel_1 = os.path.join(extracted_dir, "../malicious_script.sh")
    malicious_rel_2 = os.path.join(extracted_dir, "etc/fake_shadow")

    # Check absolute paths that shouldn't have been overwritten/created
    malicious_abs_1 = "/home/user/malicious_script.sh"
    malicious_abs_2 = "/etc/fake_shadow"

    for path in [malicious_rel_1, malicious_rel_2, malicious_abs_1, malicious_abs_2]:
        if os.path.exists(path):
            # If it exists, make sure it's not the content from the archive
            try:
                with open(path, "rb") as f:
                    content = f.read()
                if content in [b"echo 'hacked'", b"root::18704:0:99999:7:::"]:
                    pytest.fail(f"Malicious file was extracted to: {path}")
            except Exception:
                pass