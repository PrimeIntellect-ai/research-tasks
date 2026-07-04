# test_final_state.py

import os
import subprocess
import hashlib

def test_script_exists_and_executable():
    """Check if the script exists, is executable, and contains flock."""
    script_path = "/home/user/process_docs.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "flock" in content, "Script does not appear to use 'flock' for concurrency control."

def test_script_execution_and_manifest():
    """Execute the script and verify the extracted files and manifest."""
    script_path = "/home/user/process_docs.sh"

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    extracted_dir = "/home/user/docs_extracted"
    assert os.path.isdir(extracted_dir), f"Extraction directory {extracted_dir} was not created."

    manifest_path = "/home/user/docs_manifest.txt"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} was not created."

    # Dynamically compute the expected manifest
    md_files = []
    for root, _, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith(".md"):
                # Path relative to extracted_dir
                rel_path = os.path.relpath(os.path.join(root, file), extracted_dir)
                md_files.append(rel_path)

    md_files.sort()

    expected_lines = []
    for rel_path in md_files:
        abs_path = os.path.join(extracted_dir, rel_path)
        with open(abs_path, "rb") as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
        # sha256sum format: checksum  filepath
        expected_lines.append(f"{checksum}  {rel_path}")

    expected_manifest = "\n".join(expected_lines)

    with open(manifest_path, "r") as f:
        actual_manifest = f.read().strip()

    assert actual_manifest == expected_manifest, "The manifest contents do not match the expected SHA256 checksums and formatting."

def test_no_zip_files_left():
    """Ensure that all nested .zip files were removed after extraction."""
    extracted_dir = "/home/user/docs_extracted"

    if not os.path.isdir(extracted_dir):
        return # Handled by previous test

    zip_files = []
    for root, _, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith(".zip"):
                zip_files.append(os.path.join(root, file))

    assert len(zip_files) == 0, f"Nested zip files were not removed after extraction: {zip_files}"