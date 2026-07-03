# test_final_state.py
import os

def test_libprimes_so_exists():
    lib_path = '/home/user/math_feature/libprimes.so'
    assert os.path.exists(lib_path), f"{lib_path} was not generated. The build script might still be broken or not executed."

def test_output_txt_correct():
    output_path = '/home/user/math_feature/output.txt'
    assert os.path.exists(output_path), f"{output_path} was not generated. Did you run the build script?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected = "2,3,3,5,3607,3803"
    assert content == expected, f"Expected {output_path} to contain '{expected}', but got '{content}'."

def test_build_sh_fixed():
    build_sh_path = '/home/user/math_feature/build.sh'
    assert os.path.exists(build_sh_path), f"{build_sh_path} is missing."

    with open(build_sh_path, 'r') as f:
        content = f.read()

    assert "-buildmode=c-shared" in content, "build.sh does not use the '-buildmode=c-shared' flag to compile the Go code into a shared library."