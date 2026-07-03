You are tasked with refactoring and optimizing a legacy web security script used to scan and organize uploaded project files. The current pure-Python implementation is far too slow to handle our daily traffic. 

We are moving the core scanning logic to a C shared library and using Python `ctypes` for cross-language interoperability. 

Your tasks:
1. **Extract ABI Specifications:** We lost the original header file, but a screenshot of the required C struct ABI is available at `/app/spec.png`. Read the image to find the exact definition of `struct ScanResult`.
2. **Implement C Library:** Write a C program (`/app/scanner.c`) that implements the following function:
   `struct ScanResult scan_content(const char* content, int length);`
   The function should perform a fast substring search. If the `content` contains either `<script>` or `DROP TABLE`, it must return a struct with `is_safe = 0` and `threat_score = 0.99`. Otherwise, it should return `is_safe = 1` and `threat_score = 0.0`. The `file_hash` field can be left as an empty string.
3. **Compile Library:** Compile the C code into a shared library `/app/libscanner.so`. You must ensure it is heavily optimized for speed (e.g., `-O3`).
4. **Implement Python Wrapper:** Write `/app/fast_organizer.py` using `ctypes`. It must load `libscanner.so`, redefine the C struct in Python, and iterate through all files in the `/app/uploads/` directory. 
   - Read the contents of each file.
   - Pass the contents to `scan_content`.
   - If `is_safe == 1`, move the file to `/app/safe/`.
   - If `is_safe == 0`, move the file to `/app/quarantine/`.
5. **Output Results:** Your script `/app/fast_organizer.py` must write a JSON file to `/app/results.json` with the format:
   `{"safe_count": X, "quarantine_count": Y}`

**Verification Criteria:**
An automated test will measure the execution time of your `/app/fast_organizer.py` against the provided baseline `/app/slow_organizer.py`. Your implementation must achieve a **speedup of >= 5.0x** and correctly classify all files.