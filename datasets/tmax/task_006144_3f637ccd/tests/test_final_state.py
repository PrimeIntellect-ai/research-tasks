# test_final_state.py

import os
import pytest
import re

WORKSPACE_DIR = "/home/user/workspace"
RESULTS_LOG = os.path.join(WORKSPACE_DIR, "results.log")
PROTO_FILE = os.path.join(WORKSPACE_DIR, "evaluator.proto")
MAKEFILE = os.path.join(WORKSPACE_DIR, "Makefile")

def test_results_log_exists():
    assert os.path.isfile(RESULTS_LOG), f"Expected results file {RESULTS_LOG} does not exist. Did the client script run successfully?"

def test_results_log_contents():
    with open(RESULTS_LOG, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in {RESULTS_LOG}, found {len(lines)}. Server might have crashed or test cases were modified."

    # Case 1: ARCH_ARM64 1 +
    assert "ARCH_ARM64 1 +" in lines[0]
    assert "True" in lines[0]
    assert "2" in lines[0].split("|")[2].strip()

    # Case 2: 1 2 + 3 *
    assert "1 2 + 3 *" in lines[1]
    assert "True" in lines[1]
    assert "9" in lines[1].split("|")[2].strip()

    # Case 3: + (Stack underflow)
    assert "+" in lines[2]
    assert "False" in lines[2], "Expected success=False for underflow case."
    assert "RPC FAILED" not in lines[2], "Server crashed on underflow case instead of returning an error safely."

    # Case 4: 1 1 1... + + +... (Stack overflow)
    assert "1 1 1" in lines[3]
    assert "False" in lines[3], "Expected success=False for overflow case."
    assert "RPC FAILED" not in lines[3], "Server crashed on overflow case instead of returning an error safely."

def test_proto_file_exists():
    assert os.path.isfile(PROTO_FILE), f"File {PROTO_FILE} does not exist."
    with open(PROTO_FILE, 'r') as f:
        content = f.read()

    assert "syntax" in content and "proto3" in content, "Proto file must use proto3 syntax."
    assert "package build_expr;" in content or "package build_expr" in content, "Proto file must use package build_expr."
    assert "service Evaluator" in content, "Proto file must define service Evaluator."
    assert "message EvalRequest" in content, "Proto file must define message EvalRequest."
    assert "message EvalResponse" in content, "Proto file must define message EvalResponse."

def test_makefile_exists_and_targets():
    assert os.path.isfile(MAKEFILE), f"File {MAKEFILE} does not exist."
    with open(MAKEFILE, 'r') as f:
        content = f.read()

    assert re.search(r'^all:', content, re.MULTILINE), "Makefile missing 'all' target."
    assert re.search(r'^evaluator_server:', content, re.MULTILINE), "Makefile missing 'evaluator_server' target."
    assert re.search(r'^python_stubs:', content, re.MULTILINE), "Makefile missing 'python_stubs' target."

def test_generated_files_exist():
    assert os.path.isfile(os.path.join(WORKSPACE_DIR, "evaluator_server")), "evaluator_server binary not built."
    assert os.path.isfile(os.path.join(WORKSPACE_DIR, "evaluator_pb2.py")), "evaluator_pb2.py not generated."
    assert os.path.isfile(os.path.join(WORKSPACE_DIR, "evaluator_pb2_grpc.py")), "evaluator_pb2_grpc.py not generated."