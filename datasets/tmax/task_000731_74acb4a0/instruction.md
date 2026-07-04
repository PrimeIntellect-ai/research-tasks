You are tasked with migrating a legacy Python 2 interpreter application to Python 3. The application parses a simple instruction set and calculates a checksum using a custom C library via FFI (Foreign Function Interface). 

The legacy codebase is located in `/home/user/legacy_project`. It currently fails to run under Python 3 due to a mix of architectural issues (a circular import that prevents building/running) and FFI data type incompatibilities between Python 2 strings and Python 3.

Here is what you need to do:

1. **Compile the C Library**: The project includes `lib_calc.c`. Compile it into a shared library named `lib_calc.so` in the same directory.
2. **Refactor the Python Code for Python 3**:
   - Fix the circular dependency between `vm.py` and `checksum.py` that causes `ImportError` in Python 3.
   - Fix the `ctypes` FFI call in `checksum.py`. In Python 2, passing a string to `ctypes.c_char_p` worked, but Python 3 requires the proper byte encoding (UTF-8).
3. **Execute the VM**: 
   - Run `python3 main.py`. It reads `input.txt` and writes the final calculated checksum to `output.txt`.
4. **Setup a CI Script**: 
   - Create an executable bash script at `/home/user/legacy_project/ci_test.sh`.
   - The script must automate the build and execution: it should compile `lib_calc.c` to `lib_calc.so`, run `python3 main.py`, and exit with a `0` status code if successful.

Ensure that the final output value is correctly written to `/home/user/legacy_project/output.txt`. Do not change the logic of the C code or the underlying checksum algorithm.