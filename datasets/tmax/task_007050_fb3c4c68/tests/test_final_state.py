# test_final_state.py

import os
import subprocess
import pytest
import re

CI_PROTO_PATH = "/home/user/ci.proto"
GENERATE_SCRIPT_PATH = "/home/user/generate_proto.sh"
PIPELINE_DSL_PATH = "/home/user/pipeline.dsl"
TEXTPROTO_PATH = "/home/user/pipeline.textproto"

def test_ci_proto_exists_and_valid():
    assert os.path.isfile(CI_PROTO_PATH), f"File not found: {CI_PROTO_PATH}"
    with open(CI_PROTO_PATH, "r") as f:
        content = f.read()

    assert "syntax" in content and "proto3" in content, "ci.proto must use proto3 syntax."
    assert "message Step" in content, "ci.proto must define a Step message."
    assert "message Pipeline" in content, "ci.proto must define a Pipeline message."

    # Check fields
    assert re.search(r'string\s+name\s*=\s*1\s*;', content), "Step message must have string name = 1;"
    assert re.search(r'string\s+command\s*=\s*2\s*;', content), "Step message must have string command = 2;"
    assert re.search(r'string\s+id\s*=\s*1\s*;', content), "Pipeline message must have string id = 1;"
    assert re.search(r'repeated\s+Step\s+steps\s*=\s*2\s*;', content), "Pipeline message must have repeated Step steps = 2;"

def test_generate_script_exists_and_executable():
    assert os.path.isfile(GENERATE_SCRIPT_PATH), f"File not found: {GENERATE_SCRIPT_PATH}"
    assert os.access(GENERATE_SCRIPT_PATH, os.X_OK), f"Script {GENERATE_SCRIPT_PATH} is not executable."

def test_run_generate_script():
    # Run the script to generate the textproto
    result = subprocess.run([GENERATE_SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"
    assert os.path.isfile(TEXTPROTO_PATH), f"Script did not generate {TEXTPROTO_PATH}"

def test_generated_textproto_content():
    assert os.path.isfile(TEXTPROTO_PATH), f"File not found: {TEXTPROTO_PATH}"
    with open(TEXTPROTO_PATH, "r") as f:
        content = f.read()

    # Check for expected decoded values
    assert 'id:' in content and 'CI-8492' in content, "Pipeline ID CI-8492 not found in textproto."
    assert 'name:' in content and 'Build' in content, "Step name 'Build' not found in textproto."
    assert 'echo \\"Building\\"' in content or 'echo "Building"' in content, "Decoded command for Build step not found or incorrectly escaped."
    assert 'name:' in content and 'Test' in content, "Step name 'Test' not found in textproto."
    assert 'make test' in content, "Decoded command for Test step not found."
    assert 'name:' in content and 'Deploy' in content, "Step name 'Deploy' not found in textproto."
    assert './deploy.sh' in content, "Decoded command for Deploy step not found."

def test_textproto_valid_against_schema():
    # Use protoc to validate the generated textproto against the schema
    cmd = [
        "protoc",
        "--encode=Pipeline",
        CI_PROTO_PATH
    ]
    with open(TEXTPROTO_PATH, "r") as f:
        textproto_content = f.read()

    result = subprocess.run(cmd, input=textproto_content, capture_output=True, text=True)
    assert result.returncode == 0, f"Generated textproto is not valid against ci.proto. protoc error: {result.stderr}"