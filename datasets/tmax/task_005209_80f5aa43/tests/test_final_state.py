# test_final_state.py

import os
import gzip
import subprocess
import pytest

def test_rust_project_exists():
    """Verify that the Rust project directory and Cargo.toml exist."""
    cargo_toml = "/home/user/minimizer/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} is missing."

def test_minimized_files_content():
    """Verify that the minimized files exist and contain the correct UTF-8 text."""
    expected_contents = {
        "part1.gcode.gz": "G28\nG1 X10 Y10\nM104 S0\n",
        "part2.gcode.gz": "G90\nM82\nG1 Z0.2 F3000\n",
        "part3.gcode.gz": ""
    }

    for filename, expected in expected_contents.items():
        path = f"/home/user/minimized_gcode/{filename}"
        assert os.path.isfile(path), f"Minimized file {path} is missing."

        try:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            pytest.fail(f"Failed to read {path} as a gzipped UTF-8 file: {e}")

        assert content == expected, f"Content mismatch in {filename}. Expected {repr(expected)}, got {repr(content)}"

def test_manifest_exists_and_correct():
    """Verify that the manifest.txt exists and matches the actual sha256 checksums."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    # Generate expected manifest
    minimized_dir = "/home/user/minimized_gcode"
    try:
        # Run sha256sum on all .gcode.gz files in the minimized directory
        result = subprocess.run(
            ["sha256sum", "part1.gcode.gz", "part2.gcode.gz", "part3.gcode.gz"],
            cwd=minimized_dir,
            capture_output=True,
            text=True,
            check=True
        )
        actual_manifest_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run sha256sum in {minimized_dir}: {e}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_content = f.read().strip()
    manifest_lines = [line.strip() for line in manifest_content.split('\n') if line.strip()]

    for expected_line in actual_manifest_lines:
        assert expected_line in manifest_lines, (
            f"Missing or incorrect manifest entry. "
            f"Expected to find '{expected_line}' in {manifest_path}."
        )