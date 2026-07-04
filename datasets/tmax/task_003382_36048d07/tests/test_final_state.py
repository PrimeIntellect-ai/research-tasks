# test_final_state.py
import os
import subprocess
import re

def test_project_directory_exists():
    assert os.path.isdir("/home/user/req_validator"), "Project directory /home/user/req_validator does not exist."
    assert os.path.isfile("/home/user/req_validator/Cargo.toml"), "Cargo.toml is missing."
    assert os.path.isfile("/home/user/req_validator/src/lib.rs"), "src/lib.rs is missing."
    assert os.path.isfile("/home/user/req_validator/src/main.rs"), "src/main.rs is missing."

def test_cargo_toml_contents():
    with open("/home/user/req_validator/Cargo.toml", "r") as f:
        content = f.read()
    assert "proptest" in content, "proptest is not in Cargo.toml."
    assert "bench_mode" in content, "bench_mode feature is not in Cargo.toml."

def test_lib_rs_contents():
    with open("/home/user/req_validator/src/lib.rs", "r") as f:
        content = f.read()
    assert "proptest_checksum_property" in content, "proptest_checksum_property test is not defined in src/lib.rs."

def test_bench_output():
    assert os.path.isfile("/home/user/bench_output.txt"), "/home/user/bench_output.txt is missing."
    with open("/home/user/bench_output.txt", "r") as f:
        content = f.read()
    assert "Bench mode active" in content, "'Bench mode active' not found in bench_output.txt."
    assert re.search(r"Checksum:\s*0x62", content, re.IGNORECASE), "'Checksum: 0x62' not found in bench_output.txt."

def test_cargo_test_passes():
    result = subprocess.run(
        ["cargo", "test"],
        cwd="/home/user/req_validator",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"