# test_final_state.py

import os
import zlib
import ctypes

def test_crc_algo_c_fixed():
    file_path = "/home/user/crc_algo.c"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    with open(file_path, 'r') as f:
        content = f.read()
    # The bug was `i <= len`, it should be fixed to `i < len`
    assert "i <= len" not in content, "The out-of-bounds read bug 'i <= len' is still present in crc_algo.c"

def test_checksum_result_file():
    file_path = "/home/user/checksum_result.txt"
    assert os.path.exists(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        result = f.read().strip()

    expected_checksum = str(zlib.crc32(b"ALGORITHMIC_DEBUGGING"))
    assert result == expected_checksum, f"Expected checksum {expected_checksum}, but got {result}"

def test_libwrapper_so_linked_and_functional():
    lib_path = "/home/user/libwrapper.so"
    assert os.path.exists(lib_path), f"Missing file: {lib_path}"

    try:
        lib = ctypes.CDLL(lib_path)
    except OSError as e:
        pytest.fail(f"Failed to load libwrapper.so, linking issue might not be fixed: {e}")

    # Ensure compute_checksum is available and works correctly
    assert hasattr(lib, 'compute_checksum'), "compute_checksum function not found in libwrapper.so"

    lib.compute_checksum.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    lib.compute_checksum.restype = ctypes.c_uint32

    test_str = b"ALGORITHMIC_DEBUGGING"
    calculated_crc = lib.compute_checksum(test_str, len(test_str))
    expected_crc = zlib.crc32(test_str)

    assert calculated_crc == expected_crc, f"Library computed incorrect CRC: {calculated_crc} instead of {expected_crc}. The memory bug might still be present."