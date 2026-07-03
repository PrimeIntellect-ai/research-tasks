You are tasked with migrating a legacy Python 2 text processing tool to Python 3. The tool relies on a custom C library via `ctypes` to perform in-place string manipulation. The original script worked flawlessly in Python 2 where strings were byte sequences, but the migration to Python 3 has introduced character encoding issues when interfacing with C.

Here are your instructions:
1. Build the shared C library `libprocess.so` using the provided `Makefile` in `/home/user`.
2. Apply the patch `/home/user/py3_migration.patch` to the Python script `/home/user/process.py`.
3. The patched Python 3 script contains logical errors related to character encoding. The text data it processes is strictly encoded in `latin-1`. The C function expects a byte array (which should be the `latin-1` encoded bytes of the string), and the modified byte array needs to be decoded back to a `latin-1` string before writing to the output file. Fix the encoding/decoding logic in `/home/user/process.py` so that it handles `latin-1` natively without crashing or corrupting the text.
4. Run your fixed script to process the test input: 
   `python3 /home/user/process.py /home/user/input.txt /home/user/output.txt`
5. The final output must exactly match the expected bytes in `/home/user/expected.txt`.

Ensure your final fixed code is in `/home/user/process.py` and the output is successfully generated at `/home/user/output.txt`.