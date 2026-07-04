You are a QA Engineer responsible for setting up a secure testing environment for a Python-based secure file vault application. The application uses a custom C extension for computing checksums (error-correcting codes) and a SQLite database for tracking file metadata. 

Currently, the test environment setup is broken. Your task is to resolve the issues and generate a QA report.

Here are the requirements:

1. **Resolve Database Schema Circular Dependency:**
   In the directory `/home/user/app/models/`, there are two files: `file_meta.py` and `checksum_data.py`. They represent our database schema components but currently contain a circular import that prevents initialization. 
   Refactor these files to resolve the `ImportError` while preserving the classes and their relationship properties. Once fixed, run `/home/user/app/setup_db.py`. This must successfully execute and generate the SQLite database at `/home/user/app/test.db` with the required tables.

2. **Fix Memory Safety Vulnerability in C Extension:**
   The application uses a C library to compute file checksums, located at `/home/user/app/libecc/ecc.c`. 
   During preliminary security testing, we discovered that `calculate_checksum` causes a segmentation fault on large inputs due to an out-of-bounds write (buffer overflow). The function calculates a checksum and appends a 4-byte signature (`"1234"`) to the input string, but it incorrectly sizes the heap allocation.
   Fix the memory allocation bug in `ecc.c`.
   Once fixed, compile it into a shared library named `libecc.so` in the `/home/user/app/libecc/` directory using the provided `/home/user/app/libecc/build.sh` script.

3. **Verify and Generate QA Report:**
   Write a Python test script located at `/home/user/app/qa_test.py`. This script must:
   - Connect to `/home/user/app/test.db` and insert a dummy row into `file_meta` (name: "test_payload") and `checksum_data` (file_id: 1, checksum: "dummy").
   - Use Python's `ctypes` module to load `/home/user/app/libecc/libecc.so`.
   - Define the correct argtypes and restype for `calculate_checksum` (`restype` should be `ctypes.c_char_p`).
   - Call `calculate_checksum` passing exactly 100 uppercase `"A"` characters as the input payload.
   - Save the results to `/home/user/app/qa_report.json` exactly in this format:
     ```json
     {
       "db_created": true,
       "payload_checksum": "<the exact string returned by the C function>"
     }
     ```

Ensure all files are located exactly where specified. You do not need root access.