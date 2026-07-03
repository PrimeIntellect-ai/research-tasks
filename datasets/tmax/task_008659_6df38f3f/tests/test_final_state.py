# test_final_state.py
import os

def test_integration_result():
    """Check that the integration_result.txt exists and contains the correct value."""
    result_file = "/home/user/integration_result.txt"
    assert os.path.isfile(result_file), f"{result_file} does not exist. Did the emulator run successfully?"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == "4200", f"Expected integration_result.txt to contain '4200', but got '{content}'."

def test_emulator_executable_exists():
    """Check that the emulator was compiled."""
    exe_file = "/home/user/emulator"
    assert os.path.isfile(exe_file), f"{exe_file} does not exist. Was the code compiled?"
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable."

def test_makefile_fixed():
    """Check that the Makefile was fixed to use g++ instead of gcc."""
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "g++" in content, "Makefile still appears to use gcc or does not use g++."

def test_mock_server_exists():
    """Check that mock_server.py was created."""
    mock_server_path = "/home/user/mock_server.py"
    assert os.path.isfile(mock_server_path), f"{mock_server_path} does not exist."

def test_emulator_cpp_fixed():
    """Check that emulator.cpp was fixed."""
    cpp_path = "/home/user/emulator.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "a + b" in content or "b + a" in content, "emulator.cpp does not seem to have the ADD bug fixed."
    assert "8080" in content, "emulator.cpp does not seem to have the port bug fixed (should use 8080)."