# test_final_state.py

import os
import configparser

def test_destination_directory_exists():
    assert os.path.isdir("/home/user/organized_images"), "Destination directory /home/user/organized_images was not created."

def test_genuine_pngs_moved_correctly():
    expected_files = [
        "/home/user/organized_images/diagram.dat.png",
        "/home/user/organized_images/logo.png",
        "/home/user/organized_images/screenshot.png"
    ]

    for fpath in expected_files:
        assert os.path.isfile(fpath), f"Expected PNG file {fpath} is missing."

        # Verify it's actually a PNG
        with open(fpath, "rb") as f:
            header = f.read(8)
        assert header == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", f"File {fpath} is not a valid PNG."

def test_non_pngs_not_moved():
    unexpected_files = [
        "/home/user/organized_images/fake_image.png",
        "/home/user/organized_images/data.bin",
        "/home/user/organized_images/data.bin.png"
    ]

    for fpath in unexpected_files:
        assert not os.path.exists(fpath), f"Non-PNG file was incorrectly moved/copied to {fpath}."

def test_manifest_file_correct():
    manifest_path = "/home/user/png_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/organized_images/diagram.dat.png",
        "/home/user/organized_images/logo.png",
        "/home/user/organized_images/screenshot.png"
    ]

    assert lines == expected_lines, "Manifest file contents do not match the expected sorted list of absolute paths."

def test_original_genuine_pngs_removed():
    # The instructions say "Move all genuine PNG files", so they shouldn't be in docs_raw anymore.
    original_files = [
        "/home/user/docs_raw/diagram.dat",
        "/home/user/docs_raw/subdir/screenshot.png",
        "/home/user/docs_raw/other/logo"
    ]

    for fpath in original_files:
        assert not os.path.exists(fpath), f"Original genuine PNG file {fpath} was not moved (it still exists in the source directory)."