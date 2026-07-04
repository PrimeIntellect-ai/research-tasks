# test_final_state.py

import os
import re

def djb2_32(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)
        h &= 0xFFFFFFFF
    return h

def djb2_64(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)
        h &= 0xFFFFFFFFFFFFFFFF
    return h

def get_normalized_strings(raw_file):
    with open(raw_file, 'r') as f:
        lines = f.read().splitlines()

    normalized = []
    for line in lines:
        match = re.search(r'"([^"]*)"', line)
        if match:
            text = match.group(1)
            text = text.lower()
            text = re.sub(r'[^a-z0-9 ]', '', text)
            normalized.append(text)
    return normalized

def test_final_sample_exists():
    assert os.path.isfile('/home/user/final_sample.txt'), "The file /home/user/final_sample.txt does not exist."

def test_final_sample_content():
    raw_file = '/home/user/raw_strings.txt'
    assert os.path.isfile(raw_file), "The file raw_strings.txt is missing."

    normalized_strings = get_normalized_strings(raw_file)

    # Deduplicate while preserving order of first appearance (though we will sort later)
    unique_strings = []
    seen = set()
    for s in normalized_strings:
        if s not in seen:
            seen.add(s)
            unique_strings.append(s)

    expected_32 = sorted([s for s in unique_strings if djb2_32(s) % 10 == 0])
    expected_64 = sorted([s for s in unique_strings if djb2_64(s) % 10 == 0])

    with open('/home/user/final_sample.txt', 'r') as f:
        actual = f.read().splitlines()

    assert actual == expected_32 or actual == expected_64, (
        f"The content of /home/user/final_sample.txt is incorrect.\n"
        f"Expected (64-bit hash): {expected_64}\n"
        f"Expected (32-bit hash): {expected_32}\n"
        f"Actual: {actual}"
    )

def test_c_source_and_executable_exist():
    assert os.path.isfile('/home/user/process_strings.c'), "The C source file /home/user/process_strings.c does not exist."
    assert os.path.isfile('/home/user/process_strings'), "The compiled executable /home/user/process_strings does not exist."
    assert os.access('/home/user/process_strings', os.X_OK), "The file /home/user/process_strings is not executable."