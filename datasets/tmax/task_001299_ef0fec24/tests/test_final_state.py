# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
VALIDATOR_BIN = os.path.join(APP_DIR, "bin", "validator")
EVIL_CORPUS_DIR = os.path.join(APP_DIR, "corpus", "evil")
CLEAN_CORPUS_DIR = os.path.join(APP_DIR, "corpus", "clean")
ENV_FILE = os.path.join(APP_DIR, ".env")
PROTO_GO_FILE = os.path.join(APP_DIR, "proto", "build.pb.go")

def test_protobuf_compiled():
    """Verify that the protobuf definitions were compiled to Go."""
    # The exact filename might depend on the proto package, but typically it's build.pb.go
    # Let's check if any .pb.go file exists in the proto directory
    proto_dir = os.path.join(APP_DIR, "proto")
    pb_go_files = [f for f in os.listdir(proto_dir) if f.endswith(".pb.go")]
    assert len(pb_go_files) > 0, f"No compiled protobuf files (*.pb.go) found in {proto_dir}"

def test_env_configuration():
    """Verify that the environment variables are correctly configured."""
    assert os.path.isfile(ENV_FILE), f"{ENV_FILE} does not exist"
    with open(ENV_FILE, "r") as f:
        content = f.read()

    assert "REDIS_URL=localhost:6379" in content, "REDIS_URL is not correctly set in .env"
    assert "GRPC_PORT=50051" in content, "GRPC_PORT is not correctly set in .env"
    assert "WS_PORT=8081" in content, "WS_PORT is not correctly set in .env"

def test_validator_binary_exists():
    """Verify that the validator binary is compiled and exists at the specified path."""
    assert os.path.isfile(VALIDATOR_BIN), f"Validator binary not found at {VALIDATOR_BIN}"
    assert os.access(VALIDATOR_BIN, os.X_OK), f"Validator binary at {VALIDATOR_BIN} is not executable"

def test_adversarial_corpus_validator():
    """
    Test the validator against the adversarial corpus.
    Must reject 100% of evil payloads and accept 100% of clean payloads.
    """
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    assert len(evil_files) > 0, "No JSON files found in evil corpus"
    assert len(clean_files) > 0, "No JSON files found in clean corpus"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run([VALIDATOR_BIN, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run([VALIDATOR_BIN, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)