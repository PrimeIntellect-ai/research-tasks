# test_final_state.py
import os
import json
import hashlib
import subprocess

def test_script_exists_and_atomic():
    script_path = "/home/user/artifact_watcher.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    with open(script_path, "r") as f:
        code = f.read()

    # Check for atomic replace pattern
    assert any(x in code for x in ["os.replace", "shutil.move", "os.rename"]), (
        "Script does not appear to use an atomic file replacement method "
        "(os.replace, shutil.move, or os.rename)."
    )

def test_processed_files_exist():
    processed_dir = "/home/user/repo/processed/"
    files = ["file1.bin", "file2.bin", "file3.bin"]
    for file in files:
        file_path = os.path.join(processed_dir, file)
        assert os.path.exists(file_path), f"File {file} was not moved to {processed_dir}."

def test_manifest_contents():
    manifest_path = "/home/user/repo/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json is not valid JSON."

    expected_hashes = {
        "file1.bin": hashlib.sha256(b"alpha").hexdigest(),
        "file2.bin": hashlib.sha256(b"beta").hexdigest(),
        "file3.bin": hashlib.sha256(b"gamma").hexdigest(),
    }

    for filename, expected_hash in expected_hashes.items():
        assert filename in manifest, f"{filename} is missing from manifest.json."
        assert manifest[filename] == expected_hash, f"Hash for {filename} is incorrect in manifest.json."

def test_process_exited():
    # Check if artifact_watcher.py is still running
    try:
        result = subprocess.run(["pgrep", "-f", "artifact_watcher.py"], capture_output=True, text=True)
        # If result.returncode == 0, it found a process.
        assert result.returncode != 0, "The artifact_watcher.py process is still running; it did not shut down gracefully."
    except FileNotFoundError:
        # pgrep not available, fallback to ps
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        lines = [line for line in result.stdout.splitlines() if "artifact_watcher.py" in line and "grep" not in line and "pytest" not in line]
        assert len(lines) == 0, "The artifact_watcher.py process is still running; it did not shut down gracefully."