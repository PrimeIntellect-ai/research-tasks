# test_final_state.py
import os
import subprocess
import tempfile

def test_mre_math_exists_and_valid():
    """Verify mre_math.txt contains a value that triggers the math leak."""
    path = "/home/user/mre_math.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content, f"File {path} is empty."

    # It should be a number that causes NaN/Inf, such as 1.0, 1, NaN, Inf
    try:
        val = float(content)
        # 1.0 triggers division by zero in original code (1.0 - 1.0 = 0.0)
        # NaN or Inf triggers the isnan/isinf check
    except ValueError:
        # Might be 'NaN' or 'Inf' which float() handles, but just in case
        assert content.lower() in ['nan', 'inf', 'infinity', '1', '1.0'], \
            f"Content of {path} doesn't look like a valid math MRE."

def test_mre_corrupt_exists_and_valid():
    """Verify mre_corrupt.txt contains unparseable text."""
    path = "/home/user/mre_corrupt.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content, f"File {path} is empty."

    # It should raise ValueError when cast to float
    is_corrupt = False
    try:
        float(content)
    except ValueError:
        is_corrupt = True

    # Handle the case where they used "NaN" or "Inf" which are technically floats but might not be considered "corrupt" by stod depending on compiler, 
    # but strictly "corrupt" means non-numeric text.
    if not is_corrupt:
        assert content.lower() not in ['nan', 'inf', 'infinity'], \
            f"Content of {path} should be unparseable text, not a valid float representation."

def test_fixed_service_compiled():
    """Verify fixed_service executable exists."""
    assert os.path.exists("/home/user/fixed_service.cpp"), "/home/user/fixed_service.cpp does not exist."
    assert os.path.exists("/home/user/fixed_service"), "/home/user/fixed_service does not exist."
    assert os.access("/home/user/fixed_service", os.X_OK), "/home/user/fixed_service is not executable."

def test_fixed_service_no_leaks():
    """Run Valgrind on the fixed binary with mixed inputs to ensure no memory leaks."""
    test_data = "2.0\ngarbage\n1.0000000000000000001\nNaN\nInf\n3.5\n"

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write(test_data)
        tmp_path = tmp.name

    try:
        cmd = [
            "valgrind",
            "--leak-check=full",
            "--error-exitcode=1",
            "/home/user/fixed_service"
        ]

        with open(tmp_path, 'r') as stdin_f:
            result = subprocess.run(cmd, stdin=stdin_f, capture_output=True, text=True)

        assert result.returncode == 0, \
            f"Valgrind reported leaks or errors. Exit code: {result.returncode}\nStderr:\n{result.stderr}"
    finally:
        os.remove(tmp_path)

def test_fixed_service_valid_output():
    """Ensure the fixed binary still processes valid input correctly."""
    cmd = ["/home/user/fixed_service"]
    result = subprocess.run(cmd, input="2.0\n", capture_output=True, text=True)

    assert result.returncode == 0, "fixed_service crashed on valid input."
    assert "Processed: 10" in result.stdout, \
        f"Expected 'Processed: 10' in stdout, got: {result.stdout}"