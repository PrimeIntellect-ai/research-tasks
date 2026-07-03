# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_adversarial_corpus():
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/libmsgparse-1.2.0"

    # Ensure the project builds successfully
    build_cmd = ["cargo", "build", "--manifest-path", "/home/user/msg_gateway/Cargo.toml"]
    build_res = subprocess.run(build_cmd, env=env, capture_output=True, text=True)
    assert build_res.returncode == 0, f"Cargo build failed:\n{build_res.stderr}"

    binary_path = "/home/user/msg_gateway/target/debug/msg_gateway"
    assert os.path.exists(binary_path), "Compiled binary not found at expected path."

    clean_corpus = glob.glob("/app/corpora/clean/*")
    evil_corpus = glob.glob("/app/corpora/evil/*")

    assert len(clean_corpus) > 0, "No clean corpus files found."
    assert len(evil_corpus) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_corpus:
        cmd = [binary_path, f]
        res = subprocess.run(cmd, env=env, capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_corpus:
        cmd = [binary_path, f]
        res = subprocess.run(cmd, env=env, capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(f))

    err_msg = []
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} of {len(clean_corpus)} clean modified (expected exit 0, got something else): {', '.join(clean_failed)}")
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} of {len(evil_corpus)} evil bypassed (expected exit 1, got something else): {', '.join(evil_failed)}")

    assert not clean_failed and not evil_failed, " | ".join(err_msg)