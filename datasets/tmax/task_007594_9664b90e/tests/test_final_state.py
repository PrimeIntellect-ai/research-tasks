# test_final_state.py
import os
import pytest

def test_manifest_file_contents():
    manifest_path = "/home/user/success_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/public_docs/api_ref.md",
        "/home/user/public_docs/architecture.md",
        "/home/user/public_docs/introduction.md"
    ]

    assert lines == expected_lines, f"Manifest contents incorrect. Expected {expected_lines}, got {lines}"

def test_symlinks_created_correctly():
    expected_links = {
        "/home/user/public_docs/api_ref.md": "reference.md",
        "/home/user/public_docs/architecture.md": "arch.md",
        "/home/user/public_docs/introduction.md": "intro.md"
    }

    for link_path, target_name in expected_links.items():
        assert os.path.islink(link_path), f"Expected symlink not found: {link_path}"

        target_path = os.readlink(link_path)
        assert os.path.isabs(target_path), f"Symlink target must be absolute: {link_path} -> {target_path}"
        assert target_path.startswith("/home/user/extracted_docs/"), f"Symlink target not in extracted_docs: {target_path}"
        assert target_path.endswith(target_name), f"Symlink target incorrect. Expected it to end with {target_name}, got {target_path}"
        assert os.path.isfile(target_path), f"Symlink target does not exist as a file: {target_path}"

def test_symlinks_excluded_correctly():
    excluded_links = [
        "/home/user/public_docs/core_loop.md",
        "/home/user/public_docs/api_loop.md"
    ]

    for link_path in excluded_links:
        assert not os.path.exists(link_path) and not os.path.islink(link_path), f"Symlink for excluded file was created: {link_path}"

def test_script_exists():
    script_path = "/home/user/organize_docs.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"