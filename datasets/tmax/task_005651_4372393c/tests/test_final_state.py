# test_final_state.py

import os
import struct
import subprocess
import pytest

def check_elf(filepath, expected_machine):
    assert os.path.exists(filepath), f"{filepath} does not exist."
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

    with open(filepath, 'rb') as f:
        elf_header = f.read(64)

    assert elf_header[:4] == b'\x7fELF', f"{filepath} is not a valid ELF file."
    assert elf_header[4] == 2, f"{filepath} is not a 64-bit ELF."
    assert elf_header[5] == 1, f"{filepath} is not Little Endian (LSB)."

    e_machine = struct.unpack_from('<H', elf_header, 18)[0]
    assert e_machine == expected_machine, f"{filepath} has incorrect architecture. Expected {expected_machine}, got {e_machine}."

    e_phoff = struct.unpack_from('<Q', elf_header, 32)[0]
    e_phentsize = struct.unpack_from('<H', elf_header, 54)[0]
    e_phnum = struct.unpack_from('<H', elf_header, 56)[0]

    with open(filepath, 'rb') as f:
        f.seek(e_phoff)
        for _ in range(e_phnum):
            phdr = f.read(e_phentsize)
            if len(phdr) < 4:
                continue
            p_type = struct.unpack_from('<I', phdr, 0)[0]
            assert p_type != 3, f"{filepath} appears to be dynamically linked (found PT_INTERP program header). It must be statically linked."

def test_validator_x86_binary():
    """Verify the x86_64 binary exists, is executable, 64-bit, statically linked, and x86_64."""
    # 62 (0x3E) is EM_X86_64
    check_elf('/home/user/validator_x86', 62)

def test_validator_arm64_binary():
    """Verify the arm64 binary exists, is executable, 64-bit, statically linked, and aarch64."""
    # 183 (0xB7) is EM_AARCH64
    check_elf('/home/user/validator_arm64', 183)

def test_validator_x86_execution():
    """Ensure the compiled x86 binary correctly validates the binary files."""
    validator_path = '/home/user/validator_x86'
    valid_bin = '/home/user/valid.bin'
    invalid_bin = '/home/user/invalid.bin'

    assert os.path.exists(valid_bin), f"{valid_bin} is missing."
    assert os.path.exists(invalid_bin), f"{invalid_bin} is missing."

    res_valid = subprocess.run([validator_path, valid_bin], capture_output=True)
    assert res_valid.returncode == 0, f"Expected exit code 0 for {valid_bin}, got {res_valid.returncode}."

    res_invalid = subprocess.run([validator_path, invalid_bin], capture_output=True)
    assert res_invalid.returncode == 1, f"Expected exit code 1 for {invalid_bin}, got {res_invalid.returncode}."

def test_run_tests_script_exists():
    """Ensure run_tests.sh exists."""
    script_path = '/home/user/run_tests.sh'
    assert os.path.exists(script_path), f"{script_path} does not exist."

def test_test_results_log():
    """Ensure the test_results.log contains the exact expected output."""
    log_path = '/home/user/test_results.log'
    assert os.path.exists(log_path), f"{log_path} does not exist. Did run_tests.sh generate it?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = "valid_exit: 0\ninvalid_exit: 1"
    assert content == expected_content, f"Log content in {log_path} is incorrect.\nExpected:\n{expected_content}\nGot:\n{content}"