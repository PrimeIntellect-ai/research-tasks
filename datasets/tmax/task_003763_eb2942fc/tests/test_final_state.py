# test_final_state.py
import os
import subprocess

def fib_mod(n, mod=1000000007):
    if n == 0: return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % mod
    return b

def test_result_file():
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"{result_file} does not exist. The Go program may not have run successfully."

    with open(result_file, "r") as f:
        content = f.read().strip()

    expected_sum = (fib_mod(100000) + fib_mod(200000) + fib_mod(300000)) % 1000000007
    assert content == str(expected_sum), f"Expected result {expected_sum}, but got {content} in {result_file}"

def test_shared_library_exists():
    lib_path = "/home/user/math_project/lib/libfib.so"
    assert os.path.exists(lib_path), f"Shared library {lib_path} does not exist. Makefile might not be fixed correctly."

    # Check if it's a valid ELF shared object using 'file' command
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{lib_path} is not a valid shared object. Output of file command: {result.stdout}"

def test_main_go_fixed():
    main_go = "/home/user/math_project/main.go"
    assert os.path.exists(main_go), f"{main_go} is missing."
    with open(main_go, "r") as f:
        content = f.read()

    assert "wrong_include" not in content, "main.go still contains 'wrong_include'."
    assert "wrong_lib" not in content, "main.go still contains 'wrong_lib'."

    # Ensure it correctly references the proper directories
    assert "-I${SRCDIR}/include" in content or "-Iinclude" in content or "-I/home/user/math_project/include" in content, "main.go does not correctly reference the include directory."
    assert "-L${SRCDIR}/lib" in content or "-Llib" in content or "-L/home/user/math_project/lib" in content, "main.go does not correctly reference the lib directory."