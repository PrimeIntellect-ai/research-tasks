# test_final_state.py

import os
import re
import pytest

def test_asm_parser_fixed_target_arch():
    asm_parser_path = "/home/user/rust_pipeline/src/asm_parser.rs"
    assert os.path.isfile(asm_parser_path), f"{asm_parser_path} is missing"

    with open(asm_parser_path, "r") as f:
        content = f.read()

    assert 'target_arch = "x86-64"' not in content, "The target_arch bug 'x86-64' is still present in asm_parser.rs"
    assert 'target_arch = "x86_64"' in content, "The target_arch should be fixed to 'x86_64' in asm_parser.rs"

def test_asm_parser_fixed_asm_block():
    asm_parser_path = "/home/user/rust_pipeline/src/asm_parser.rs"
    assert os.path.isfile(asm_parser_path), f"{asm_parser_path} is missing"

    with open(asm_parser_path, "r") as f:
        content = f.read()

    # Check if 42 is being moved into a register in the asm! block
    # We look for something like `mov {0}, 42` or `mov rax, 42`
    assert re.search(r'mov\s+[^,]+,\s*42', content, re.IGNORECASE) is not None, \
        "The asm! block does not seem to correctly load 42 into the register."

def test_migration_tests_fixed():
    tests_path = "/home/user/rust_pipeline/tests/migration_tests.rs"
    assert os.path.isfile(tests_path), f"{tests_path} is missing"

    with open(tests_path, "r") as f:
        content = f.read()

    # Check that processed_timestamp: 0 is added to the _mock_v2_expected RecordV2 struct
    assert re.search(r'processed_timestamp\s*:\s*0', content) is not None, \
        "The missing `processed_timestamp: 0` field was not added to the RecordV2 instantiation in tests/migration_tests.rs"

def test_success_log_exists_and_passed():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you run tests and redirect output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "test result: ok" in content, "The success.log does not indicate that the tests passed."
    assert "2 passed" in content, "The success.log does not indicate that 2 tests passed."