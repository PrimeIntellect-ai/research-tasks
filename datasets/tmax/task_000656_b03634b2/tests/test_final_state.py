# test_final_state.py
import os
import subprocess
import pytest

def test_output_log_exists():
    """Test that output.log was generated."""
    assert os.path.isfile("/home/user/output.log"), "The file /home/user/output.log does not exist."

def test_output_log_contents():
    """Test that output.log contains the correct metrics for the pcap files."""
    with open("/home/user/output.log", "r") as f:
        content = f.read()

    assert "capture 1.pcap" in content, "output.log is missing 'capture 1.pcap'."
    assert "4.000" in content, "output.log does not contain the expected metric 4.000 for capture 1.pcap."

    assert "capture 2.pcap" in content, "output.log is missing 'capture 2.pcap'."
    assert "5.000" in content, "output.log does not contain the expected metric 5.000 for capture 2.pcap."

def test_mre_c_exists():
    """Test that mre.c was created."""
    assert os.path.isfile("/home/user/mre.c"), "The file /home/user/mre.c does not exist."

def test_mre_c_compiles_and_runs():
    """Test that mre.c compiles and produces the correct output for sqrt(100.0)."""
    # Compile mre.c
    compile_cmd = ["gcc", "-o", "/home/user/mre_bin", "/home/user/mre.c", "-lm"]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile /home/user/mre.c:\n{compile_proc.stderr}"

    assert os.path.isfile("/home/user/mre_bin"), "Compiled binary /home/user/mre_bin was not created."

    # Run the compiled binary
    run_proc = subprocess.run(["/home/user/mre_bin"], capture_output=True, text=True)
    assert run_proc.returncode == 0, f"Running /home/user/mre_bin failed:\n{run_proc.stderr}"

    # Check output
    output = run_proc.stdout
    assert output == "10.000\n", f"Expected output '10.000\\n', but got {repr(output)}"