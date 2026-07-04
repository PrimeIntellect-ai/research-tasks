# test_final_state.py

import os
import re
import urllib.request
import urllib.error

POLYBUILD_DIR = "/home/user/polybuild"

def test_polybuild_dir_exists():
    """Verify that the polybuild directory exists."""
    assert os.path.isdir(POLYBUILD_DIR), f"Directory {POLYBUILD_DIR} does not exist."

def test_generated_schema_python():
    """Verify the generated Python schema file."""
    py_schema_path = os.path.join(POLYBUILD_DIR, "generated_schema.py")
    assert os.path.isfile(py_schema_path), f"File {py_schema_path} does not exist."

    with open(py_schema_path, "r") as f:
        content = f.read()

    assert "@dataclass" in content, "Python schema does not use @dataclass."
    assert "class Person" in content or "class Person:" in content, "Python schema does not define class Person."
    assert re.search(r"name\s*:\s*str", content), "Python schema missing 'name: str' field."
    assert re.search(r"age\s*:\s*int", content), "Python schema missing 'age: int' field."

def test_generated_schema_c():
    """Verify the generated C schema file."""
    c_schema_path = os.path.join(POLYBUILD_DIR, "generated_schema.h")
    assert os.path.isfile(c_schema_path), f"File {c_schema_path} does not exist."

    with open(c_schema_path, "r") as f:
        content = f.read()

    # Remove whitespace to check structure
    content_no_ws = re.sub(r'\s+', '', content)

    # Check for typedef struct { char* name; int age; } Person;
    assert "typedefstruct{" in content_no_ws, "C schema missing 'typedef struct {'."
    assert "char*name;" in content_no_ws, "C schema missing 'char* name;'."
    assert "intage;" in content_no_ws, "C schema missing 'int age;'."
    assert "}Person;" in content_no_ws, "C schema missing '} Person;'."

def test_execution_log():
    """Verify the execution log contains the correct topological sort order with alphabetical tie-breaking."""
    log_path = os.path.join(POLYBUILD_DIR, "execution_log.txt")
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "translate",
        "compile_c",
        "run_py",
        "run_c",
        "combine"
    ]

    assert lines == expected_order, f"Execution log order is incorrect. Expected {expected_order}, got {lines}."

def test_final_output():
    """Verify the final combined output contains both C and Python outputs."""
    out_path = os.path.join(POLYBUILD_DIR, "final_output.txt")
    assert os.path.isfile(out_path), f"File {out_path} does not exist."

    with open(out_path, "r") as f:
        content = f.read()

    assert "C: Bob is 25" in content, "final_output.txt missing C output."
    assert "Python: Alice is 30" in content, "final_output.txt missing Python output."

def test_http_server_running():
    """Verify that an HTTP server is serving the execution log on port 8080."""
    url = "http://127.0.0.1:8080/execution_log.txt"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            status = response.getcode()
            content = response.read().decode('utf-8')

        assert status == 200, f"Expected HTTP status 200, got {status}."
        assert "translate" in content and "combine" in content, "HTTP server did not serve the correct execution_log.txt content."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to HTTP server on port 8080: {e}"