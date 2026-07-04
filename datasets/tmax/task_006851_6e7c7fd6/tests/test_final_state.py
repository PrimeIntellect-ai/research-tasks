# test_final_state.py
import os
import pytest

def test_libwsee_compiled():
    so_path = "/home/user/wsee/build/libwsee.so"
    assert os.path.isfile(so_path), f"Expected compiled shared library at {so_path} does not exist."

def test_strict_security_flag():
    build_dir = "/home/user/wsee/build"
    assert os.path.isdir(build_dir), f"Build directory {build_dir} does not exist."

    found_strict = False
    for root, dirs, files in os.walk(build_dir):
        for file in files:
            # Check makefiles, ninja files, or cmake files for the flag
            if file.endswith(".make") or file == "build.ninja" or file == "CMakeCache.txt" or file == "flags.make":
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "STRICT_SECURITY" in content or "ENABLE_STRICT_MODE" in content:
                            found_strict = True
                            break
                except Exception:
                    pass
        if found_strict:
            break

    assert found_strict, "Could not find -DSTRICT_SECURITY or ENABLE_STRICT_MODE in the CMake build files. The conditional build flag was not properly implemented or passed."

def test_evaluation_result():
    result_path = "/home/user/wsee/evaluation_result.txt"
    assert os.path.isfile(result_path), f"Evaluation result file {result_path} is missing. orchestrator.py might not have run or failed."

    with open(result_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "1", f"Expected evaluation_result.txt to contain exactly '1', but got '{content}'."