You are a script developer working on a mathematical utility that interfaces with a highly optimized C shared library. 

I have written a Python script located at `/home/user/math_utility.py` that dynamically loads this shared library, checks its version, and handles ABI differences. If the library version is `>= 2.0.0`, it uses a new advanced math function. If it is an older version, it falls back to a basic Python implementation.

The contents of `/home/user/math_utility.py` are:
```python
import ctypes
from packaging import version
import math

def run_calculation(lib_path, value):
    try:
        lib = ctypes.CDLL(lib_path)
    except OSError:
        return None
    
    lib.get_version.restype = ctypes.c_char_p
    v_str = lib.get_version().decode('utf-8')
    
    if version.parse(v_str) >= version.parse("2.0.0"):
        lib.advanced_calc.restype = ctypes.c_double
        lib.advanced_calc.argtypes = [ctypes.c_double]
        return lib.advanced_calc(float(value))
    else:
        return math.sqrt(float(value))
```

Your task is to write a comprehensive test suite for this module using `pytest` and `unittest.mock`. 

Requirements:
1. Create a test file at `/home/user/test_math_utility.py`.
2. Do not compile or require any actual `.so` files. You must use `unittest.mock.patch` to mock `ctypes.CDLL` and simulate the shared library's behavior.
3. Write a test named `test_legacy_version_fallback`:
   - Mock `ctypes.CDLL` so that the returned library object's `get_version` method returns `b"1.9.9"` (note the bytes!).
   - Call `run_calculation("dummy_path.so", 16.0)`.
   - Assert that the function returns `4.0` (from `math.sqrt`).
   - Assert that the mock library's `advanced_calc` method was *never* called.
4. Write a test named `test_modern_version_abi`:
   - Mock `ctypes.CDLL` so that the returned library object's `get_version` method returns `b"2.1.0"`.
   - Set up the mock library object so that calling `advanced_calc` returns `99.9`.
   - Call `run_calculation("dummy_path.so", 16.0)`.
   - Assert that the function returns `99.9`.
   - Assert that the mock library's `advanced_calc` method was called exactly once with `16.0`.
5. Run your test file using `pytest` and save the standard output to `/home/user/test_results.txt`.

Ensure your mocks correctly simulate the structure expected by `ctypes.CDLL` attributes (`get_version`, `advanced_calc`, `restype`, `argtypes`).