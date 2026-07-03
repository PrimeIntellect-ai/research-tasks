# test_final_state.py
import os
import subprocess

def test_resolution_txt():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    expected = "SECRET: PROD_MATH_88492_XYZ\nCRASH_INPUTS: -2147483648, -1"
    assert content == expected, f"Content of {path} does not match expected output. Got:\n{content}"

def test_run_test_executable():
    path = "/home/user/math_server/run_test"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    result = subprocess.run([path], capture_output=True)
    assert result.returncode == 0, f"Executing {path} returned non-zero exit code: {result.returncode}"

def test_math_ops_logic():
    # Compile our own test against math_ops.c to verify the logic directly
    c_code = """
    #include <stdio.h>
    #include "math_ops.c"
    int main() {
        int res = gcd(-2147483648, -1);
        if (res == -1) return 0;
        return 1;
    }
    """
    test_file = "/tmp/verify_math_ops.c"
    out_binary = "/tmp/verify_math_ops"
    with open(test_file, "w") as f:
        f.write(c_code)

    compile_res = subprocess.run(
        ["gcc", test_file, "-o", out_binary, "-I/home/user/math_server"], 
        cwd="/home/user/math_server", 
        capture_output=True
    )
    assert compile_res.returncode == 0, f"Failed to compile math_ops.c with test harness:\n{compile_res.stderr.decode()}"

    run_res = subprocess.run([out_binary], capture_output=True)
    assert run_res.returncode == 0, "gcd(-2147483648, -1) did not return -1 as required."