We are migrating our backend data pipeline from Python 2 to Python 3. As part of this, we need to port a legacy C-extension used for high-performance parsing of our custom structured telemetry data (a proprietary TLV format) and secure it against malicious payloads.

You have been provided with the following workspace:
- `/home/user/legacy/fast_tlv.c`: The legacy Python 2 C-extension source code. It is extremely fast but notoriously memory-unsafe.
- `/app/oracle_parser`: A stripped, standalone executable compiled from the same legacy C logic. It is provided for your reference to observe how the legacy system processes (or fatally crashes on) various inputs.

Your objectives:
1. **Port & Repair**: Port `fast_tlv.c` to a Python 3 C-extension. During the port, you must identify and fix the C memory safety vulnerabilities (buffer overflows and undefined behaviors) that cause the legacy parser to crash on malformed structured data. 
2. **Build**: Create a `/home/user/py3_ext/setup.py` and compile the modernized, safe C-extension as `fast_tlv`. 
3. **Sanitization Wrapper**: Write a Python 3 script at `/home/user/sanitizer.py` with the following CLI signature:
   `python3 /home/user/sanitizer.py <input_file> <output_file>`
   This script must use your new `fast_tlv` module to parse the structured data.
   - If the data is fully valid and safe, the script must write the exact unmodified bytes to `<output_file>` and exit with code 0.
   - If the data is malformed or contains an exploit payload (which would have crashed the legacy binary), your fixed extension must raise a Python `ValueError`. The script must catch this, prevent the file from being copied, and exit with code 1.
4. **Performance Benchmark**: The original extension was written in C for speed. Ensure your memory-safe implementation does not introduce excessive overhead. A script at `/home/user/benchmark.py` is available for you to verify that your extension processes the standard payload batch in under 500ms.

Do not rely on the legacy Python 2 environment. Your final deliverable must run entirely in Python 3. Make sure `/home/user/sanitizer.py` is robust and handles all file I/O safely.