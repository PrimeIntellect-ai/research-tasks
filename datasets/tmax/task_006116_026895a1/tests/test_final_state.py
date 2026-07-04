# test_final_state.py

import os
import re
import time
import subprocess
import pytest

def test_organizer_cpp_exists_and_uses_rename():
    """Check that organizer.cpp exists and contains the rename() function for atomic updates."""
    cpp_file = "/home/user/organizer.cpp"
    assert os.path.exists(cpp_file), f"File {cpp_file} does not exist."

    with open(cpp_file, "r") as f:
        content = f.read()

    assert re.search(r'rename\s*\(', content), "organizer.cpp does not use the rename() function for atomic updates."

def test_pipeline_execution():
    """Run start.sh, drop a nested zip, and verify the correct symlinks and manifest are created."""
    start_sh = "/home/user/start.sh"
    assert os.path.exists(start_sh), f"File {start_sh} does not exist."

    # Ensure start.sh is executable
    os.chmod(start_sh, 0o755)

    # Start the background process
    proc = subprocess.Popen(["/bin/bash", start_sh], cwd="/home/user")

    try:
        # Give the script a moment to compile and start the watcher
        time.sleep(2)

        # Create test dataset
        os.makedirs("/tmp/test_gen/batch_1", exist_ok=True)
        with open("/tmp/test_gen/alpha.csv", "w") as f:
            f.write("id,value\n1,10\n")
        with open("/tmp/test_gen/zeta.csv", "w") as f:
            f.write("id,value\n2,20\n")

        subprocess.run(["tar", "-czf", "/tmp/test_gen/batch_1/data1.tar.gz", "-C", "/tmp/test_gen", "alpha.csv"], check=True)
        subprocess.run(["tar", "-czf", "/tmp/test_gen/batch_1/data2.tar.gz", "-C", "/tmp/test_gen", "zeta.csv"], check=True)

        os.makedirs("/home/user/incoming", exist_ok=True)

        # Create the zip directly in the incoming directory to trigger the watcher
        subprocess.run(["zip", "-r", "/home/user/incoming/dataset_001.zip", "batch_1"], cwd="/tmp/test_gen", check=True)

        # Wait for the watcher to process the file
        time.sleep(5)

        # Verify symlinks
        alpha_link = "/home/user/dataset_links/alpha.csv"
        zeta_link = "/home/user/dataset_links/zeta.csv"

        assert os.path.islink(alpha_link), f"{alpha_link} is not a valid symlink."
        assert os.path.islink(zeta_link), f"{zeta_link} is not a valid symlink."

        # Verify manifest
        manifest_path = "/home/user/dataset_links/manifest.log"
        assert os.path.exists(manifest_path), f"Manifest file {manifest_path} does not exist."

        with open(manifest_path, "r") as f:
            content = f.read().strip()

        expected_content = "alpha.csv\nzeta.csv"
        assert content == expected_content, f"Manifest content mismatch. Expected:\n{expected_content}\nGot:\n{content}"

    finally:
        # Clean up the background process
        subprocess.run(["pkill", "-f", "organizer"], check=False)
        proc.terminate()