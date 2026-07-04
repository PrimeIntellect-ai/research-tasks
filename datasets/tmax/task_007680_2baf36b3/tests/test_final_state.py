# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_script_exists_and_executable():
    script_path = "/home/user/organize_docs.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_release_directories_created():
    assert os.path.isdir("/home/user/release/docs"), "Directory /home/user/release/docs does not exist"
    assert os.path.isdir("/home/user/release/models"), "Directory /home/user/release/models does not exist"

def test_markdown_files_processed_correctly():
    docs_dir = "/home/user/release/docs"
    expected_files = {
        "introduction_to_alpha_intro.md": "/home/user/doc_staging/project_alpha/v1/intro.md",
        "beta_notes_notes.md": "/home/user/doc_staging/project_beta/drafts/notes.md"
    }

    # Check that expected files are present and match original contents
    for expected_file, original_path in expected_files.items():
        target_path = os.path.join(docs_dir, expected_file)
        assert os.path.isfile(target_path), f"Expected file {expected_file} is missing in {docs_dir}"

        with open(target_path, "r") as tf, open(original_path, "r") as of:
            assert tf.read() == of.read(), f"Content of {expected_file} does not match the original file"

    # Check that draft files are not copied
    all_docs = os.listdir(docs_dir)
    assert len(all_docs) == len(expected_files), f"Expected exactly {len(expected_files)} files in docs directory, found {len(all_docs)}"
    assert not any("spec" in f for f in all_docs), "Draft document (spec.md) should not be included in the release"

def test_gcode_files_processed_correctly():
    models_dir = "/home/user/release/models"
    expected_files = {
        "abs_housing.gcode": "/home/user/doc_staging/project_alpha/v1/housing.gcode",
        "pla_gear.gcode": "/home/user/doc_staging/shared_assets/printing/gear.gcode",
        "unknown_test_cube.gcode": "/home/user/doc_staging/shared_assets/printing/test_cube.gcode"
    }

    for expected_file, original_path in expected_files.items():
        target_path = os.path.join(models_dir, expected_file)
        assert os.path.isfile(target_path), f"Expected file {expected_file} is missing in {models_dir}"

        with open(target_path, "r") as tf, open(original_path, "r") as of:
            assert tf.read() == of.read(), f"Content of {expected_file} does not match the original file"

    all_models = os.listdir(models_dir)
    assert len(all_models) == len(expected_files), f"Expected exactly {len(expected_files)} files in models directory, found {len(all_models)}"

def test_manifest_generated_correctly():
    manifest_path = "/home/user/release/manifest.sha256"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    expected_entries = [
        "docs/beta_notes_notes.md",
        "docs/introduction_to_alpha_intro.md",
        "models/abs_housing.gcode",
        "models/pla_gear.gcode",
        "models/unknown_test_cube.gcode"
    ]

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_entries), f"Manifest should contain exactly {len(expected_entries)} entries, found {len(lines)}"

    # Check sorting and content
    actual_paths = []
    for line in lines:
        parts = line.split("  ")
        assert len(parts) == 2, f"Manifest line format incorrect: '{line}'. Expected '<hash>  <path>'"

        file_hash, rel_path = parts
        actual_paths.append(rel_path)

        full_path = os.path.join("/home/user/release", rel_path)
        assert os.path.isfile(full_path), f"File referenced in manifest does not exist: {full_path}"

        expected_hash = get_sha256(full_path)
        assert file_hash == expected_hash, f"Hash mismatch for {rel_path}. Expected {expected_hash}, got {file_hash}"

    assert actual_paths == expected_entries, "Manifest entries are not sorted alphabetically by relative path or contain wrong paths"