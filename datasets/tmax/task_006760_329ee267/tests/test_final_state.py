# test_final_state.py

import os
import hashlib
import ast

def test_pwned_file_exists_and_matches():
    """Test that the pwned.txt file was created and matches the secret_key.txt."""
    secret_path = "/home/user/secret_key.txt"
    pwned_path = "/home/user/pwned.txt"

    assert os.path.isfile(pwned_path), f"File {pwned_path} does not exist. The exploit may have failed."
    assert os.path.isfile(secret_path), f"File {secret_path} is missing."

    with open(secret_path, 'rb') as f:
        secret_content = f.read()

    with open(pwned_path, 'rb') as f:
        pwned_content = f.read()

    assert secret_content == pwned_content, "The content of pwned.txt does not match secret_key.txt."

def test_hash_result():
    """Test that hash_result.txt contains the correct SHA256 hash of pwned.txt."""
    pwned_path = "/home/user/pwned.txt"
    hash_path = "/home/user/hash_result.txt"

    assert os.path.isfile(pwned_path), f"File {pwned_path} does not exist."
    assert os.path.isfile(hash_path), f"File {hash_path} does not exist."

    with open(pwned_path, 'rb') as f:
        pwned_content = f.read()

    expected_hash = hashlib.sha256(pwned_content).hexdigest()

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The hash in {hash_path} is incorrect. Expected {expected_hash}, got {actual_hash}."

def test_fixed_app_exists_and_secure():
    """Test that fixed_app.py exists and uses secure file I/O instead of OS command execution."""
    fixed_app_path = "/home/user/fixed_app.py"

    assert os.path.isfile(fixed_app_path), f"File {fixed_app_path} does not exist."

    with open(fixed_app_path, 'r') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        assert False, f"Syntax error in {fixed_app_path}: {e}"

    class SecurityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.uses_os_system = False
            self.uses_subprocess = False
            self.uses_open = False

        def visit_Call(self, node):
            # Check for os.system
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'os' and node.func.attr == 'system':
                    self.uses_os_system = True
            # Check for subprocess module usage
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess':
                    self.uses_subprocess = True
            # Check for native open()
            if isinstance(node.func, ast.Name) and node.func.id == 'open':
                self.uses_open = True
            self.generic_visit(node)

        def visit_Import(self, node):
            for alias in node.names:
                if alias.name == 'subprocess':
                    self.uses_subprocess = True
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.module == 'subprocess':
                self.uses_subprocess = True
            self.generic_visit(node)

    visitor = SecurityVisitor()
    visitor.visit(tree)

    assert not visitor.uses_os_system, "fixed_app.py still uses os.system(), which violates the secure coding policy."
    assert not visitor.uses_subprocess, "fixed_app.py uses the subprocess module, which violates the secure coding policy."
    assert visitor.uses_open, "fixed_app.py does not appear to use the native open() function for file I/O."