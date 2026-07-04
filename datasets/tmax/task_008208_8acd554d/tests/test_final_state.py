# test_final_state.py

import os
import re

WORKSPACE_DIR = "/home/user/workspace"
DATA_BIN = os.path.join(WORKSPACE_DIR, "data.bin")
MAKEFILE = os.path.join(WORKSPACE_DIR, "Makefile")
PROCESSOR_C = os.path.join(WORKSPACE_DIR, "processor.c")
PROCESSOR_EXE = os.path.join(WORKSPACE_DIR, "processor")
RESULT_TXT = os.path.join(WORKSPACE_DIR, "result.txt")

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE), f"File {MAKEFILE} does not exist."
    with open(MAKEFILE, 'r') as f:
        content = f.read()

    assert "processor: processor.c" in content, "Makefile missing target."
    assert "\tgcc" in content, "Makefile must use a tab instead of spaces for the command."

def test_processor_c_fixed():
    assert os.path.isfile(PROCESSOR_C), f"File {PROCESSOR_C} does not exist."
    with open(PROCESSOR_C, 'r') as f:
        content = f.read()

    # Check for struct packing
    has_packed_attr = "__attribute__((packed))" in content.replace(" ", "")
    has_pragma_pack = "#pragmapack" in content.replace(" ", "")
    assert has_packed_attr or has_pragma_pack, "processor.c must define the struct as packed to fix the deserialization bug."

    # Check for inline assembly
    assert "__asm__" in content or "asm(" in content or "asm (" in content or "asm\n" in content, "processor.c must implement inline assembly for the gcd function."

def test_executable_exists():
    assert os.path.isfile(PROCESSOR_EXE), f"Executable {PROCESSOR_EXE} was not built."
    assert os.access(PROCESSOR_EXE, os.X_OK), f"{PROCESSOR_EXE} is not executable."

def test_result_txt_correct():
    assert os.path.isfile(RESULT_TXT), f"File {RESULT_TXT} was not created. Did you run the executable?"
    with open(RESULT_TXT, 'r') as f:
        content = f.read().strip()

    assert content == "GCD: 18", f"Expected result.txt to contain 'GCD: 18', but got '{content}'."