# test_final_state.py

import os
import json
import ast
import pytest

def test_aggregator_so_exists_and_elf():
    """Verify aggregator.so exists and is an ELF file."""
    path = "/home/user/build/aggregator.so"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {path} is not a valid ELF file."

def test_aggregator_exe_exists_and_pe():
    """Verify aggregator.exe exists and is a PE file."""
    path = "/home/user/build/aggregator.exe"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "rb") as f:
        magic = f.read(2)
    assert magic == b"MZ", f"File {path} is not a valid PE (Windows) executable."

def test_results_json_correct():
    """Verify results.json has the correct subnet counts."""
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected = {
        "10.0.0.0/8": 50,
        "172.16.0.0/12": 30,
        "192.168.1.0/24": 20
    }

    assert data == expected, f"Content of {path} does not match the expected output. Got: {data}"

def test_ip_trie_ast():
    """Verify ip_trie.py contains IPTrie class with insert and count_subnet methods."""
    path = "/home/user/ip_trie.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {path}: {e}")

    trie_class = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "IPTrie":
            trie_class = node
            break

    assert trie_class is not None, "Class 'IPTrie' not found in ip_trie.py"

    methods = [n.name for n in trie_class.body if isinstance(n, ast.FunctionDef)]
    assert "insert" in methods, "Method 'insert' not found in IPTrie class"
    assert "count_subnet" in methods, "Method 'count_subnet' not found in IPTrie class"