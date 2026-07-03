# test_final_state.py
import os
import re

def test_final_docs_exists_and_correct():
    final_docs_path = '/home/user/final_docs.md'
    assert os.path.exists(final_docs_path), f"The file {final_docs_path} does not exist. Did you create it?"
    assert os.path.isfile(final_docs_path), f"The path {final_docs_path} is not a regular file."

    expected_content = """# API Reference

Endpoints are RESTful and use JSON payloads.
---
# Architecture

The system uses a monolithic design with modular components.
---
# Authentication

JWT tokens are required in the Authorization header.
---
# Deployment

Use the provided Docker Compose file to deploy the stack.
---"""

    with open(final_docs_path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), (
        f"The content of {final_docs_path} does not match the expected sorted markdown output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{content}"
    )

def test_cpp_parser_exists_and_uses_flock():
    cpp_path = '/home/user/bdoc_parser.cpp'
    assert os.path.exists(cpp_path), f"The C++ source file {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"The path {cpp_path} is not a regular file."

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert 'flock' in content, "The C++ program must use flock() to ensure thread-safe appends."
    assert 'LOCK_EX' in content, "The C++ program must use LOCK_EX with flock()."

def test_executable_exists():
    exe_path = '/home/user/bdoc_parser'
    assert os.path.exists(exe_path), f"The executable {exe_path} does not exist. Did you compile the C++ program?"
    assert os.path.isfile(exe_path), f"The path {exe_path} is not a regular file."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."