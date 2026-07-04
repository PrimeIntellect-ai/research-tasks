# test_final_state.py
import os
import ast

def test_success_log_exists_and_correct():
    log_path = "/home/user/success.log"
    assert os.path.exists(log_path), f"The file {log_path} does not exist. Did the script run to completion?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected = "Total balance: 5000"
    assert content == expected, f"Expected '{expected}' in {log_path}, but got '{content}'"

def test_no_global_lock_used():
    script_path = "/home/user/transaction_processor.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    with open(script_path, 'r') as f:
        source = f.read()

    tree = ast.parse(source)

    # Check that Account class still initializes a lock
    account_has_lock = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'Account':
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Attribute) and subnode.attr == 'lock':
                    account_has_lock = True
                    break

    assert account_has_lock, "The Account class must still use individual locks. Do not use a single global lock."

    # Check that transfer function is defined and uses locks
    transfer_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'transfer':
            transfer_found = True
            with_count = 0
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.With):
                    with_count += 1
            assert with_count >= 1, "The transfer function must use locks (with statements)."

    assert transfer_found, "The transfer function must be defined."