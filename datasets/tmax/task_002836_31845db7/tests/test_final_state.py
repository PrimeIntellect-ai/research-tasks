# test_final_state.py
import os

def test_astmath_binaries_exist():
    base_dir = "/home/user/libastmath"

    astmath_path = os.path.join(base_dir, "astmath")
    assert os.path.isfile(astmath_path), f"Binary {astmath_path} is missing. Did you run `make`?"
    assert os.access(astmath_path, os.X_OK), f"File {astmath_path} is not executable."

    astmath_embedded_path = os.path.join(base_dir, "astmath_embedded")
    assert os.path.isfile(astmath_embedded_path), f"Binary {astmath_embedded_path} is missing. Did you run `make target=embedded`?"
    assert os.access(astmath_embedded_path, os.X_OK), f"File {astmath_embedded_path} is not executable."

def test_math_result():
    result_file = "/home/user/math_result.txt"
    assert os.path.isfile(result_file), f"File {result_file} is missing."

    with open(result_file, "r") as f:
        content = f.read().strip()

    # 2^(3^2) = 2^9 = 512
    # The C printf("%f\n", result) formats as 512.000000 by default
    assert "512.000000" in content, f"Expected 512.000000 in {result_file}, but found '{content}'."

def test_valgrind_report():
    report_file = "/home/user/valgrind_report.txt"
    assert os.path.isfile(report_file), f"File {report_file} is missing."

    with open(report_file, "r") as f:
        content = f.read()

    assert "definitely lost: 0 bytes" in content, f"Expected 'definitely lost: 0 bytes' in {report_file}. Memory leak might not be fully fixed."