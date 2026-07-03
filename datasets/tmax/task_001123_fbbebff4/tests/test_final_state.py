# test_final_state.py
import os
import subprocess
import random
import pytest

def test_libchecksum_built():
    lib_path = "/home/user/project/legacy_c/libchecksum.so"
    assert os.path.isfile(lib_path), f"Expected shared library {lib_path} does not exist. The C library was not built successfully."

def test_rust_wrapper_built():
    bin_path = "/home/user/project/rust_wrapper/target/release/rust_wrapper"
    assert os.path.isfile(bin_path), f"Expected Rust binary {bin_path} does not exist. The Rust wrapper did not compile in release mode."

def test_env_file_contents():
    env_path = "/home/user/project/services/.env"
    assert os.path.isfile(env_path), f"{env_path} does not exist."
    with open(env_path, "r") as f:
        content = f.read()

    assert "VALIDATOR_BIN=/home/user/project/rust_wrapper/target/release/rust_wrapper" in content, ".env is missing or has incorrect VALIDATOR_BIN configuration."
    assert "LD_LIBRARY_PATH=/home/user/project/legacy_c" in content, ".env is missing or has incorrect LD_LIBRARY_PATH configuration."

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle/validator_oracle"
    agent_bin = "/home/user/project/rust_wrapper/target/release/rust_wrapper"

    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"
    assert os.path.isfile(agent_bin), f"Agent binary missing at {agent_bin}"

    random.seed(42)

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/project/legacy_c" + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")

    for _ in range(1000):
        byte_len = random.randint(8, 256)
        hex_str = "".join(random.choice("0123456789abcdefABCDEF") for _ in range(byte_len * 2))

        oracle_res = subprocess.run([oracle_bin, hex_str], capture_output=True, text=True)
        agent_res = subprocess.run([agent_bin, hex_str], capture_output=True, text=True, env=env)

        assert oracle_res.returncode == agent_res.returncode, (
            f"Return code mismatch on input {hex_str}.\n"
            f"Oracle return code: {oracle_res.returncode}\n"
            f"Agent return code: {agent_res.returncode}"
        )

        assert oracle_res.stdout == agent_res.stdout, (
            f"Stdout mismatch on input {hex_str}.\n"
            f"Oracle stdout: {oracle_res.stdout!r}\n"
            f"Agent stdout: {agent_res.stdout!r}"
        )