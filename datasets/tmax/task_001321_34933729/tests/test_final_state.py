# test_final_state.py
import os
import sys
import tempfile
import subprocess

def test_files_exist():
    """Ensure all required files are created in the correct directory."""
    base_dir = "/home/user/polyrunner"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist."

    expected_files = ["translator.py", "server.py", "ci_setup.sh"]
    for f in expected_files:
        filepath = os.path.join(base_dir, f)
        assert os.path.isfile(filepath), f"File {filepath} is missing."

def test_translator_python():
    """Test the translator.py logic for python target."""
    base_dir = "/home/user/polyrunner"
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    try:
        import translator
    except ImportError:
        assert False, "Could not import translator.py"

    content = """TARGET python
BEGIN_PSEUDO
PRINT "Initializing python build"
SET_VAR retries 3
PRINT retries
END_PSEUDO
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".polybuild") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        target, code = translator.translate(tmp_path)
        assert target == "python", f"Expected target 'python', got '{target}'"

        # Execute the translated python code to verify its correctness
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py") as tmp_py:
            tmp_py.write(code)
            tmp_py_path = tmp_py.name

        try:
            result = subprocess.run(["python3", tmp_py_path], capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            assert output == "Initializing python build\n3", f"Unexpected python execution output: {output}"
        finally:
            os.remove(tmp_py_path)
    finally:
        os.remove(tmp_path)

def test_translator_bash():
    """Test the translator.py logic for bash target."""
    base_dir = "/home/user/polyrunner"
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    try:
        import translator
    except ImportError:
        assert False, "Could not import translator.py"

    content = """TARGET bash
BEGIN_PSEUDO
PRINT "Initializing bash build"
SET_VAR debug_level 5
PRINT debug_level
END_PSEUDO
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".polybuild") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        target, code = translator.translate(tmp_path)
        assert target == "bash", f"Expected target 'bash', got '{target}'"

        # Execute the translated bash code to verify its correctness
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".sh") as tmp_sh:
            tmp_sh.write(code)
            tmp_sh_path = tmp_sh.name

        try:
            result = subprocess.run(["bash", tmp_sh_path], capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            assert output == "Initializing bash build\n5", f"Unexpected bash execution output: {output}"
        finally:
            os.remove(tmp_sh_path)
    finally:
        os.remove(tmp_path)

def test_server_and_ci_setup_contents():
    """Check that server.py and ci_setup.sh contain expected keywords indicating they implemented the requirements."""
    server_path = "/home/user/polyrunner/server.py"
    with open(server_path, 'r') as f:
        server_code = f.read()

    assert "9333" in server_code, "server.py does not seem to bind to port 9333."
    assert "websockets" in server_code or "asyncio" in server_code, "server.py does not seem to use websockets/asyncio."

    ci_setup_path = "/home/user/polyrunner/ci_setup.sh"
    with open(ci_setup_path, 'r') as f:
        ci_code = f.read()

    assert "pip" in ci_code and "websockets" in ci_code, "ci_setup.sh does not appear to install websockets."
    assert "server.py" in ci_code, "ci_setup.sh does not appear to start server.py."
    assert "sleep 2" in ci_code or "sleep" in ci_code, "ci_setup.sh does not appear to wait for the server to bind."