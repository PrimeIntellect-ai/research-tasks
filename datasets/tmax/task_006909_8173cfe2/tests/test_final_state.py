# test_final_state.py
import os
import subprocess

def test_loop_trigger():
    """Verify that the loop trigger byte was correctly identified and saved."""
    path = "/home/user/loop_trigger.txt"
    assert os.path.exists(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content.upper() == "FF", f"Expected 'FF' in {path}, got '{content}'."

def test_fixed_parser_compiles_and_runs():
    """Verify that the fixed parser compiles and correctly processes a test payload without panicking or looping."""
    src_path = "/home/user/fixed_parser.rs"
    bin_path = "/home/user/fixed_parser"
    test_bin = "/home/user/test.bin"

    assert os.path.exists(src_path), f"{src_path} does not exist."

    # Compile the fixed Rust source
    compile_proc = subprocess.run(
        ["rustc", src_path, "-o", bin_path],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"
    assert os.path.exists(bin_path), "Executable was not created after compilation."

    # Create a test payload: 0x01, 0xFF (trigger), 0x02
    # Expected sum: 1 + 1 (from 0xFF logic) + 2 = 4
    with open(test_bin, "wb") as f:
        f.write(b"\x01\xFF\x02")

    # Run the compiled binary
    try:
        run_proc = subprocess.run(
            [bin_path, test_bin],
            capture_output=True,
            text=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        assert False, "Execution timed out. The infinite loop bug might not be fixed."

    assert run_proc.returncode == 0, f"Execution failed (possibly out-of-bounds panic):\n{run_proc.stderr}"
    assert "Parsed: Some(4)" in run_proc.stdout, f"Unexpected output:\n{run_proc.stdout}"