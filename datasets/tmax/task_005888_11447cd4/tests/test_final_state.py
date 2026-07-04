# test_final_state.py

import os
import re
import ast

def test_resolution_content():
    dump_path = "/home/user/crash_memory.dump"
    assert os.path.exists(dump_path), f"Memory dump file {dump_path} is missing."

    with open(dump_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    m = re.search(r'PAYLOAD_START\{(.*?)\}PAYLOAD_END', content)
    assert m is not None, "Could not find payload in crash_memory.dump"

    payload_str = m.group(1)
    numbers = [int(x.strip()) for x in payload_str.split(',') if x.strip()]

    # Recompute the expected checksum based on the described formula
    # Formula: add 0x5A to the value, multiply by 13, modulo 256
    expected_sum = sum(((n + 0x5A) * 13) % 256 for n in numbers)

    resolution_path = "/home/user/resolution.txt"
    assert os.path.exists(resolution_path), f"Resolution file {resolution_path} is missing."

    with open(resolution_path, "r", encoding="utf-8") as f:
        res_content = f.read().strip()

    assert res_content == str(expected_sum), f"Expected resolution.txt to contain '{expected_sum}', but found '{res_content}'."

def test_processor_script_fixes():
    script_path = "/home/user/processor.py"
    assert os.path.exists(script_path), f"Python script {script_path} is missing."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for concurrency fix (Lock)
    assert "Lock" in content or "Semaphore" in content, "The script does not appear to use a threading Lock to fix the race condition."

    # Parse AST to ensure the formula was changed
    try:
        tree = ast.parse(content)
    except SyntaxError:
        pytest.fail("processor.py contains syntax errors.")

    # We won't strictly check the exact AST for the formula since there are multiple ways to write it,
    # but we can check that the original buggy string is gone.
    assert "val + 0x5A * 13 % 256" not in content.replace(" ", ""), "The order of operations bug is still present in processor.py."