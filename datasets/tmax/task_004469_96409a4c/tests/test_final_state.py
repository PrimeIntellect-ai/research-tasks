# test_final_state.py

import os
import ast
import pytest

def test_leaked_token_extracted():
    token_path = "/home/user/leaked_token.txt"
    assert os.path.isfile(token_path), f"The file {token_path} does not exist."

    with open(token_path, "r") as f:
        content = f.read().strip()

    assert content == "SECRET_TOKEN_77X91_PLUTO", f"Expected token 'SECRET_TOKEN_77X91_PLUTO', but got '{content}'."

def test_cache_size_calculated():
    size_path = "/home/user/cache_size.txt"
    assert os.path.isfile(size_path), f"The file {size_path} does not exist."

    with open(size_path, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected cache size '3', but got '{content}'."

def test_mre_script_exists_and_valid():
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"The file {mre_path} does not exist."

    with open(mre_path, "r") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"The file {mre_path} contains invalid Python syntax: {e}")

    # Check if app.worker is imported
    imports_app_worker = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if "app.worker" in alias.name:
                    imports_app_worker = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and "app.worker" in node.module:
                imports_app_worker = True
            elif node.module == "app" and any(alias.name == "worker" for alias in node.names):
                imports_app_worker = True

    assert imports_app_worker, f"The script {mre_path} does not seem to import from 'app.worker'."