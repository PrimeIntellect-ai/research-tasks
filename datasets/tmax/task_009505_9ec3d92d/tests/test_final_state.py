# test_final_state.py

import os
import subprocess
import pytest

def test_parser_output():
    """Verify the output of the parser run."""
    output_file = "/home/user/parser_output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_output = "init:436\nstart:558\nexecute:755\n"

    with open(output_file, 'r') as f:
        content = f.read()

    assert content.strip() == expected_output.strip(), f"Output file content is incorrect. Got:\n{content}"

def test_binaries_exist_and_architecture():
    """Verify that both binaries exist and are compiled for the correct architectures."""
    sys_parser = "/home/user/workspace/sys_parser"
    sys_parser_arm = "/home/user/workspace/sys_parser_arm"

    assert os.path.isfile(sys_parser), f"Binary {sys_parser} does not exist."
    assert os.path.isfile(sys_parser_arm), f"Binary {sys_parser_arm} does not exist."

    # Check architecture using file command
    out_x86 = subprocess.check_output(["file", sys_parser]).decode('utf-8')
    assert "x86-64" in out_x86 or "x86_64" in out_x86, f"{sys_parser} is not an x86-64 executable."

    out_arm = subprocess.check_output(["file", sys_parser_arm]).decode('utf-8')
    assert "aarch64" in out_arm or "ARM aarch64" in out_arm, f"{sys_parser_arm} is not an ARM aarch64 executable."

def test_source_files_exist():
    """Verify that all required source files exist."""
    required_files = [
        "/home/user/workspace/parser.cpp",
        "/home/user/workspace/action_x86.s",
        "/home/user/workspace/action_arm.cpp",
        "/home/user/workspace/Makefile"
    ]

    for f in required_files:
        assert os.path.isfile(f), f"Required source file {f} does not exist."

def test_assembly_file_contents():
    """Verify that the assembly file has basic assembly directives."""
    asm_file = "/home/user/workspace/action_x86.s"
    assert os.path.isfile(asm_file), f"{asm_file} does not exist."

    with open(asm_file, 'r') as f:
        content = f.read()

    assert ".global process_action" in content or ".globl process_action" in content, "Assembly file does not contain expected global directive for process_action."