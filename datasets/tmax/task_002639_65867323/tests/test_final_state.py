# test_final_state.py

import os
import hashlib

def test_script_exists():
    """Test that the required Python script exists."""
    script_path = "/home/user/process_artifacts.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_curated_binaries_directory():
    """Test that the curated_binaries directory exists and contains only the expected .bin files."""
    curated_dir = "/home/user/curated_binaries"
    assert os.path.exists(curated_dir), f"Directory {curated_dir} does not exist."
    assert os.path.isdir(curated_dir), f"{curated_dir} is not a directory."

    files = sorted(os.listdir(curated_dir))
    expected_files = ["alpha.bin", "beta.bin", "delta.bin", "gamma.bin"]
    assert files == expected_files, f"Expected files in {curated_dir} to be {expected_files}, but found {files}."

def test_manifest_exists_and_correct():
    """Test that the manifest file exists, is sorted, and contains correct checksums."""
    manifest_path = "/home/user/manifest.sha256"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} does not exist."
    assert os.path.isfile(manifest_path), f"{manifest_path} is not a file."

    expected_content = (
        "e8243ea5ee904128540c5bdece9eaf3c224217112ea1bc84ed9a572a6e9a7e6b  alpha.bin\n"
        "03f56360098dfc0fcf9c0bfdff310ee9cfb0068ba02ce7614e5b98bc28f41180  beta.bin\n"
        "1476db7806f71d53dc20bf9eb4ff02cd909e7c5dfa9a62ce7d7164b3dae3ebba  delta.bin\n"
        "fb8f2c300c3b84db53044b7d446eb2db865d4b55bebfb799988ee09bbca11c06  gamma.bin\n"
    )

    with open(manifest_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Manifest content does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_binaries_content():
    """Test that the extracted binaries have the correct content/checksums."""
    curated_dir = "/home/user/curated_binaries"
    expected_hashes = {
        "alpha.bin": "e8243ea5ee904128540c5bdece9eaf3c224217112ea1bc84ed9a572a6e9a7e6b",
        "beta.bin": "03f56360098dfc0fcf9c0bfdff310ee9cfb0068ba02ce7614e5b98bc28f41180",
        "delta.bin": "1476db7806f71d53dc20bf9eb4ff02cd909e7c5dfa9a62ce7d7164b3dae3ebba",
        "gamma.bin": "fb8f2c300c3b84db53044b7d446eb2db865d4b55bebfb799988ee09bbca11c06"
    }

    for filename, expected_hash in expected_hashes.items():
        filepath = os.path.join(curated_dir, filename)
        assert os.path.exists(filepath), f"File {filepath} is missing."

        with open(filepath, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        assert actual_hash == expected_hash, f"Hash mismatch for {filename}. Expected {expected_hash}, got {actual_hash}."