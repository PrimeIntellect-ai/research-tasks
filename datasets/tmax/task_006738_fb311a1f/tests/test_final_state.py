# test_final_state.py

import os
import csv
import tarfile
import zipfile
import tempfile
import re
import pytest

def test_extruder_history_csv():
    csv_path = "/home/user/extruder_history.csv"
    assert os.path.exists(csv_path), f"Expected CSV file not found at {csv_path}"

    expected_rows = [
        ["Node", "Version", "E_Value"],
        ["node_alpha", "v1", "90.0"],
        ["node_alpha", "v2", "92.5"],
        ["node_alpha", "v3", "94.0"],
        ["node_beta", "v1", "100.0"],
        ["node_beta", "v2", "98.5"],
        ["node_beta", "v3", "99.0"]
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"CSV contents do not match expected. Got: {actual_rows}"

def test_updated_tarball_structure_and_contents():
    tarball_path = "/home/user/updated_cnc_configs.tar.gz"
    assert os.path.exists(tarball_path), f"Expected updated tarball not found at {tarball_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getnames()
            assert "node_alpha.zip" in members, "node_alpha.zip missing from updated tarball"
            assert "node_beta.zip" in members, "node_beta.zip missing from updated tarball"

            # Extract to check zip contents
            tar.extractall(path=tmpdir)

        # Check node_alpha.zip
        alpha_zip_path = os.path.join(tmpdir, "node_alpha.zip")
        assert os.path.exists(alpha_zip_path), "node_alpha.zip failed to extract"

        with zipfile.ZipFile(alpha_zip_path, "r") as z:
            alpha_files = z.namelist()
            assert "v1.gcode" in alpha_files, "v1.gcode missing from node_alpha.zip"
            assert "v2.gcode" in alpha_files, "v2.gcode missing from node_alpha.zip"
            assert "v3.gcode" in alpha_files, "v3.gcode missing from node_alpha.zip"

            v3_content = z.read("v3.gcode").decode("utf-8")
            assert re.search(r"M92 X80\.0 Y80\.0 Z400\.0 E104\.5\s*; Set axis steps per unit", v3_content), \
                "node_alpha/v3.gcode does not contain the correctly updated M92 line"

            v1_content = z.read("v1.gcode").decode("utf-8")
            assert "E90.0" in v1_content, "node_alpha/v1.gcode was incorrectly modified"

        # Check node_beta.zip
        beta_zip_path = os.path.join(tmpdir, "node_beta.zip")
        assert os.path.exists(beta_zip_path), "node_beta.zip failed to extract"

        with zipfile.ZipFile(beta_zip_path, "r") as z:
            beta_files = z.namelist()
            assert "v1.gcode" in beta_files, "v1.gcode missing from node_beta.zip"
            assert "v2.gcode" in beta_files, "v2.gcode missing from node_beta.zip"
            assert "v3.gcode" in beta_files, "v3.gcode missing from node_beta.zip"

            v3_content = z.read("v3.gcode").decode("utf-8")
            assert re.search(r"M92 X100\.0 Y100\.0 Z400\.0 E109\.5\s*; Set axis steps per unit", v3_content), \
                "node_beta/v3.gcode does not contain the correctly updated M92 line"

            v2_content = z.read("v2.gcode").decode("utf-8")
            assert "E98.5" in v2_content, "node_beta/v2.gcode was incorrectly modified"