# test_final_state.py

import os
import ctypes

def test_source_files_exist():
    """Verify that the required source files were created."""
    assert os.path.isfile('/home/user/migrate.h'), "/home/user/migrate.h does not exist"
    assert os.path.isfile('/home/user/migrate.c'), "/home/user/migrate.c does not exist"
    assert os.path.isfile('/home/user/test_migrate.py'), "/home/user/test_migrate.py does not exist"

def test_libmigrate_exists_and_works():
    """Verify that libmigrate.so exists, can be loaded, and implements the correct logic."""
    lib_path = '/home/user/libmigrate.so'
    assert os.path.isfile(lib_path), f"{lib_path} does not exist"

    class RecordV1(ctypes.Structure):
        _fields_ = [("id", ctypes.c_int), ("name", ctypes.c_char * 20)]

    class RecordV2(ctypes.Structure):
        _fields_ = [("id", ctypes.c_int), ("name", ctypes.c_char * 20), ("score", ctypes.c_float)]

    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        assert False, f"Failed to load {lib_path} via ctypes: {e}"

    assert hasattr(lib, 'migrate_v1_to_v2'), "Function migrate_v1_to_v2 not found in libmigrate.so"

    lib.migrate_v1_to_v2.argtypes = [ctypes.POINTER(RecordV1), ctypes.POINTER(RecordV2)]
    lib.migrate_v1_to_v2.restype = None

    in_rec = RecordV1(id=42, name=b"TestName")
    out_rec = RecordV2()

    lib.migrate_v1_to_v2(ctypes.byref(in_rec), ctypes.byref(out_rec))

    assert out_rec.id == 42, f"Expected id 42, got {out_rec.id}"
    assert out_rec.name == b"TestName", f"Expected name b'TestName', got {out_rec.name}"
    assert out_rec.score == 0.0, f"Expected score 0.0, got {out_rec.score}"

def test_log_file_exists_and_passed():
    """Verify that test_result.log exists and contains evidence of passing tests."""
    log_path = '/home/user/test_result.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, 'r') as f:
        log_content = f.read().lower()

    assert "passed" in log_content or "100%" in log_content, "Tests did not pass according to pytest output in test_result.log"