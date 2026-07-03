# test_final_state.py
import os
import ast

def test_c2_address_txt():
    """Verify that the c2_address.txt file contains the correct decoded IP and port."""
    file_path = "/home/user/c2_address.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "198.51.100.45:4444"
    assert content == expected, f"Expected {file_path} to contain '{expected}', but got '{content}'."

def test_firewall_block_sh():
    """Verify that the firewall_block.sh file contains the correct iptables rule."""
    file_path = "/home/user/firewall_block.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        # Read the file and filter out empty lines
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly one non-empty line in {file_path}, but found {len(lines)}."

    expected_rule = "iptables -A OUTPUT -d 198.51.100.45 -p tcp --dport 4444 -j DROP"
    assert lines[0] == expected_rule, f"Expected rule '{expected_rule}', but got '{lines[0]}'."

def test_extract_c2_py():
    """Verify that the extract_c2.py script exists and is a valid Python file."""
    file_path = "/home/user/extract_c2.py"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        source = f.read()

    try:
        ast.parse(source)
    except SyntaxError as e:
        assert False, f"The file {file_path} contains invalid Python syntax: {e}"