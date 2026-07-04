# test_final_state.py
import os
import subprocess
import ctypes
import tempfile
import glob
import pytest

def test_project_structure():
    assert os.path.isdir("/home/user/dsp_server/src"), "src/ directory not found."
    assert os.path.isdir("/home/user/dsp_server/include"), "include/ directory not found."

    # Check that .c files were moved
    assert os.path.isfile("/home/user/dsp_server/src/main.c"), "main.c not in src/"
    assert os.path.isfile("/home/user/dsp_server/src/server.c"), "server.c not in src/"
    assert os.path.isfile("/home/user/dsp_server/src/validator.c"), "validator.c not in src/"

    # Check that .h files were moved
    assert os.path.isfile("/home/user/dsp_server/include/server.h"), "server.h not in include/"
    assert os.path.isfile("/home/user/dsp_server/include/validator.h"), "validator.h not in include/"

def test_cmake_build():
    # Attempt to build the project
    build_dir = "/home/user/dsp_server/build_test"
    os.makedirs(build_dir, exist_ok=True)

    cmake_res = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=True, text=True)
    assert cmake_res.returncode == 0, f"CMake configuration failed:\n{cmake_res.stderr}"

    make_res = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)
    assert make_res.returncode == 0, f"Make build failed:\n{make_res.stderr}"

    assert os.path.isfile(os.path.join(build_dir, "dsp_server")), "dsp_server executable not built."

def test_validator_logic():
    validator_c = "/home/user/dsp_server/src/validator.c"
    assert os.path.isfile(validator_c), f"{validator_c} not found."

    with tempfile.TemporaryDirectory() as tmpdir:
        shared_lib = os.path.join(tmpdir, "validator.so")
        compile_res = subprocess.run(
            ["gcc", "-shared", "-fPIC", "-o", shared_lib, validator_c],
            capture_output=True, text=True
        )
        assert compile_res.returncode == 0, f"Failed to compile validator.c to shared library:\n{compile_res.stderr}"

        lib = ctypes.CDLL(shared_lib)

        # int validate_bytecode(const uint8_t* code, size_t len);
        lib.validate_bytecode.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
        lib.validate_bytecode.restype = ctypes.c_int

        def validate(data: bytes) -> int:
            arr = (ctypes.c_uint8 * len(data))(*data)
            return lib.validate_bytecode(arr, len(data))

        clean_dir = "/app/corpus/clean"
        evil_dir = "/app/corpus/evil"

        clean_files = glob.glob(os.path.join(clean_dir, "*.bin"))
        evil_files = glob.glob(os.path.join(evil_dir, "*.bin"))

        assert len(clean_files) > 0, "No clean corpus files found."
        assert len(evil_files) > 0, "No evil corpus files found."

        clean_failed = []
        for f in clean_files:
            with open(f, "rb") as fp:
                data = fp.read()
            if validate(data) != 1:
                clean_failed.append(os.path.basename(f))

        evil_failed = []
        for f in evil_files:
            with open(f, "rb") as fp:
                data = fp.read()
            if validate(data) != 0:
                evil_failed.append(os.path.basename(f))

        errors = []
        if clean_failed:
            errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
        if evil_failed:
            errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

        assert not errors, " / ".join(errors)