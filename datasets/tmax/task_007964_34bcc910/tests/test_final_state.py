# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/build_acl.sh"
OUTPUT_PATH = "/home/user/final_acl.txt"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_script_logic():
    # Create temporary files for testing to ensure the script doesn't hardcode answers
    with tempfile.TemporaryDirectory() as tmpdir:
        team_a_path = os.path.join(tmpdir, "team_a.txt")
        team_b_path = os.path.join(tmpdir, "team_b.txt")
        constraints_path = os.path.join(tmpdir, "constraints.txt")

        with open(team_a_path, "w") as f:
            f.write("ALLOW /api/v1/users\n")
            f.write("ALLOW /public/home\n")
            f.write("ALLOW /admin/settings\n")
            f.write("ALLOW /shared/data\n")

        with open(team_b_path, "w") as f:
            f.write("ALLOW /public/home\n")
            f.write("ALLOW /internal/stats\n")
            f.write("ALLOW /api/v2/users\n")
            f.write("ALLOW /shared/data\n")

        with open(constraints_path, "w") as f:
            f.write("DENY /admin\n")
            f.write("DENY /internal\n")

        # Remove output file if it exists from previous runs
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

        # Run the script
        result = subprocess.run(
            [SCRIPT_PATH, team_a_path, team_b_path, constraints_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

        # Check output file exists
        assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created by the script"

        with open(OUTPUT_PATH, "r") as f:
            output_lines = [line.strip() for line in f if line.strip()]

        expected_lines = [
            "ALLOW /api/v1/users",
            "ALLOW /api/v2/users",
            "ALLOW /public/home",
            "ALLOW /shared/data"
        ]

        assert output_lines == expected_lines, (
            f"Output file contents do not match expected.\n"
            f"Expected: {expected_lines}\n"
            f"Got: {output_lines}"
        )