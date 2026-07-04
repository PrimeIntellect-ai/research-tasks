# test_final_state.py
import os
import pytest
import ast

def test_stolen_creds_extracted():
    creds_file = "/home/user/investigation/stolen_creds.txt"
    assert os.path.isfile(creds_file), f"File {creds_file} does not exist. Did you extract the credentials?"

    with open(creds_file, 'r') as f:
        content = f.read().strip()

    assert content == "admin:SuperSecret123!", f"Extracted credentials do not match the expected value. Found: {content}"

def test_worker_remediated():
    worker_file = "/home/user/investigation/worker.py"
    assert os.path.isfile(worker_file), f"File {worker_file} is missing."

    with open(worker_file, 'r') as f:
        content = f.read()

    # Check that environment variables are being read
    assert "DB_USER" in content, "worker.py does not appear to read DB_USER from the environment."
    assert "DB_PASS" in content, "worker.py does not appear to read DB_PASS from the environment."

    # Check that command line arguments are removed
    assert "--user" not in content, "worker.py still contains '--user' argument parsing."
    assert "--pass" not in content, "worker.py still contains '--pass' argument parsing."

def test_processor_remediated():
    processor_file = "/home/user/investigation/processor.py"
    assert os.path.isfile(processor_file), f"File {processor_file} is missing."

    with open(processor_file, 'r') as f:
        content = f.read()

    # Check that the credentials are no longer passed as command line arguments
    assert "--user" not in content, "processor.py still passes '--user' as a command line argument."
    assert "--pass" not in content, "processor.py still passes '--pass' as a command line argument."

    # Use AST to verify subprocess.Popen is called with env
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"processor.py has a syntax error: {e}")

    popen_found = False
    env_passed = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'Popen':
                popen_found = True
                for kw in node.keywords:
                    if kw.arg == 'env':
                        env_passed = True
                        break

    assert popen_found, "processor.py no longer calls subprocess.Popen."
    assert env_passed, "processor.py calls subprocess.Popen but does not pass the 'env' keyword argument to inject environment variables."