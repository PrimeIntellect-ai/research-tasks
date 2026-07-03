# test_final_state.py

import os

def test_build_env_exists_and_correct():
    env_path = "/home/user/mobile_build/build.env"
    assert os.path.isfile(env_path), f"File {env_path} does not exist. Did orchestrator.py run successfully?"

    with open(env_path, "r") as f:
        content = f.read().strip().split("\n")

    env_vars = {}
    for line in content:
        if "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

    assert env_vars.get("ARCH") == "arm64", "build.env does not contain the correct ARCH value."
    assert env_vars.get("OPT") == "O3", "build.env does not contain the correct OPT value."
    assert env_vars.get("LTO") == "true", "build.env does not contain the correct LTO value."

def test_libmobile_so_exists():
    so_path = "/home/user/mobile_build/libmobile.so"
    assert os.path.isfile(so_path), f"File {so_path} does not exist. Did you run 'make'?"

def test_success_log_exists():
    log_path = "/home/user/mobile_build/success.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did report.py send the correct POST request?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"Expected success.log to contain 'SUCCESS', but found '{content}'"