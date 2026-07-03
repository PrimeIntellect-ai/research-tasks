# test_final_state.py

import os
import subprocess
import pytest

def test_closest_txt_content():
    closest_path = "/home/user/closest.txt"
    assert os.path.isfile(closest_path), f"File {closest_path} is missing."

    with open(closest_path, "r") as f:
        content = f.read().strip()

    assert content == "run_4", f"Expected 'run_4' in {closest_path}, but got '{content}'."

def test_process_rs_exists():
    process_rs_path = "/home/user/process.rs"
    assert os.path.isfile(process_rs_path), f"Rust source file {process_rs_path} is missing."

def test_repro_sh_exists_and_passes():
    repro_sh_path = "/home/user/test_repro.sh"
    assert os.path.isfile(repro_sh_path), f"Bash script {repro_sh_path} is missing."

    # Ensure it's executable or run it via bash
    try:
        result = subprocess.run(
            ["bash", repro_sh_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert "PASS" in output, f"Expected 'PASS' in the output of {repro_sh_path}, but got '{output}'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script {repro_sh_path} failed to execute. Error: {e.stderr}")