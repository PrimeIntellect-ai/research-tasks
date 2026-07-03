# test_final_state.py

import os
import re

def test_wal_recovered_log():
    wal_recovered_path = "/home/user/wal_recovered.log"
    assert os.path.isfile(wal_recovered_path), f"Expected {wal_recovered_path} to exist."

    with open(wal_recovered_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 497, f"Expected exactly 497 valid lines in wal_recovered.log, found {len(lines)}."

    for line in lines:
        parts = line.split('|')
        assert len(parts) == 5, f"Line does not have exactly 5 fields: {line}"
        seq, action, key, val, chk = parts

        expected_chk = len(key) + len(val)
        assert chk.isdigit() and int(chk) == expected_chk, f"Invalid checksum for line: {line}. Expected {expected_chk}, got {chk}."

def test_apply_wal_sh_fixed():
    script_path = "/home/user/apply_wal.sh"
    assert os.path.isfile(script_path), f"Expected {script_path} to exist."

    with open(script_path, "r") as f:
        content = f.read()

    # The original buggy script contained: if [ "$seq" -ge "$MAX_SEQ" ]; then
    # The fix should replace -ge with -gt or equivalent logic.
    assert not re.search(r'"\$seq"\s+-ge\s+"\$MAX_SEQ"', content), "The boundary bug (-ge) is still present in apply_wal.sh."
    assert not re.search(r'\$seq\s+-ge\s+\$MAX_SEQ', content), "The boundary bug (-ge) is still present in apply_wal.sh."

    # Check for presence of a likely fix (-gt, >)
    has_fix = bool(re.search(r'-gt|>', content))
    assert has_fix, "Could not find a valid fix (like -gt or >) for the boundary condition in apply_wal.sh."

def test_poison_seq_txt():
    poison_path = "/home/user/poison_seq.txt"
    assert os.path.isfile(poison_path), f"Expected {poison_path} to exist."

    with open(poison_path, "r") as f:
        content = f.read().strip()

    assert content == "312", f"Expected poison_seq.txt to contain exactly '312', but found '{content}'."