# test_final_state.py
import os
import subprocess

def encode_string(data: str, shift: int) -> str:
    """Helper to compute the expected hex output."""
    return "".join(f"{(ord(c) + shift) % 256:02X}" for c in data)

def test_executable_exists():
    executable = "/home/user/math_project/math_router"
    assert os.path.isfile(executable), f"Executable not found at {executable}. Did make run successfully?"
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable."

def test_run_log_content():
    log_file = "/home/user/math_project/run.log"
    assert os.path.isfile(log_file), f"Log file not found at {log_file}."

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_hex = encode_string("AgentTraining", 14)
    assert content == expected_hex, f"run.log content '{content}' does not match expected '{expected_hex}'."

def test_math_router_valid_route():
    executable = "/home/user/math_project/math_router"
    test_url = "/api/encode?shift=10&data=abc"
    expected_hex = encode_string("abc", 10)

    result = subprocess.run(
        [executable, test_url],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Expected exit code 0 for valid route, got {result.returncode}."
    output = result.stdout.strip()
    assert output == expected_hex, f"Expected output '{expected_hex}', got '{output}'."

def test_math_router_invalid_route():
    executable = "/home/user/math_project/math_router"
    test_url = "/api/badroute?shift=1&data=a"

    result = subprocess.run(
        [executable, test_url],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected exit code 1 for invalid route, got {result.returncode}."
    output = result.stdout.strip()
    assert output == "404 Not Found", f"Expected '404 Not Found' for invalid route, got '{output}'."