# test_final_state.py

import os
import re
import subprocess
import pytest

DOC_INDEX_PATH = '/home/user/doc_index.txt'
FIRMWARE_PATH = '/home/user/artifacts/firmware.elf'

def get_elf_entry_point(filepath):
    try:
        output = subprocess.check_output(['readelf', '-h', filepath], universal_newlines=True)
        for line in output.splitlines():
            if 'Entry point address' in line:
                # Extract the hex address
                match = re.search(r'0x[0-9a-fA-F]+', line)
                if match:
                    return match.group(0)
    except Exception:
        pass
    return None

def test_doc_index_exists():
    assert os.path.isfile(DOC_INDEX_PATH), f"{DOC_INDEX_PATH} does not exist."

def test_doc_index_content():
    with open(DOC_INDEX_PATH, 'r') as f:
        content = f.read()

    # Check MAX_Z
    assert re.search(r'^MAX_Z:\s*24\.5$', content, re.MULTILINE), "MAX_Z value is incorrect or missing. Expected 24.5."

    # Check ELF_ENTRY
    expected_entry = get_elf_entry_point(FIRMWARE_PATH)
    assert expected_entry is not None, "Could not determine expected ELF entry point from firmware.elf."

    elf_match = re.search(r'^ELF_ENTRY:\s*(0x[0-9a-fA-F]+)$', content, re.MULTILINE)
    assert elf_match is not None, "ELF_ENTRY line is missing or incorrectly formatted."

    actual_entry = elf_match.group(1)
    # Compare integer values to handle possible leading zeros
    assert int(actual_entry, 16) == int(expected_entry, 16), f"ELF_ENTRY value is incorrect. Expected {expected_entry}, got {actual_entry}."

    # Check FATAL_ERROR
    # The text might have spaces or no spaces where newlines were stripped.
    expected_error_no_spaces = "Memory layout corrupted.Address bus assertion failed.Aborting build."
    expected_error_spaces = "Memory layout corrupted. Address bus assertion failed. Aborting build."

    fatal_error_match = re.search(r'^FATAL_ERROR:\s*(.*)$', content, re.MULTILINE)
    assert fatal_error_match is not None, "FATAL_ERROR line is missing or incorrectly formatted."

    actual_error = fatal_error_match.group(1).strip()
    assert actual_error in (expected_error_no_spaces, expected_error_spaces), \
        f"FATAL_ERROR value is incorrect. Got: {actual_error}"