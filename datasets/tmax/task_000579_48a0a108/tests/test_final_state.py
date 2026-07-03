# test_final_state.py

import os
import pytest

def compute_max_hailstone(start: int) -> int:
    n = start
    max_val = n
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        if n > max_val:
            max_val = n
    return max_val

def test_result_file():
    expected_max = compute_max_hailstone(77031)
    result_path = "/home/user/result.txt"

    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == str(expected_max), f"Expected maximum value {expected_max}, but got '{content}' in {result_path}."

def test_makefile_fixed():
    makefile_path = "/home/user/hailstone_ffi/c_src/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "ar " in content and "libfastmath.a" in content, "Makefile does not seem to be fixed to use 'ar' for creating the static library."
    assert "gcc -o libfastmath.a" not in content, "Makefile still contains the buggy 'gcc -o libfastmath.a' line."

def test_build_rs_exists():
    build_rs_path = "/home/user/hailstone_ffi/rust_src/build.rs"
    assert os.path.isfile(build_rs_path), f"build.rs {build_rs_path} is missing."

    with open(build_rs_path, "r") as f:
        content = f.read()

    assert "cargo:rustc-link-search=" in content or "cargo:rustc-link-lib=" in content, "build.rs does not contain Cargo linking instructions."

def test_rust_files_modified():
    lib_path = "/home/user/hailstone_ffi/rust_src/src/lib.rs"
    main_path = "/home/user/hailstone_ffi/rust_src/src/main.rs"

    assert os.path.isfile(lib_path), f"{lib_path} is missing."
    assert os.path.isfile(main_path), f"{main_path} is missing."

    with open(lib_path, "r") as f:
        lib_content = f.read()
    with open(main_path, "r") as f:
        main_content = f.read()

    assert "Iterator" in lib_content and "next" in lib_content, "lib.rs does not seem to implement the Iterator trait."
    assert "extern" in lib_content or "extern" in main_content, "No FFI 'extern' block found in the Rust source files."