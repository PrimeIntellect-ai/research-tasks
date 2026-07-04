**URGENT: 3 AM PAGE - `report_generator` Service Crash**

You are the on-call systems engineer. At 3:00 AM, PagerDuty alerts you that the backend data processing daemon, `report_generator.py`, has been continuously crash-looping with a `Segmentation fault`. This service is critical for morning reporting.

The service reads raw telemetry from `/home/user/app/data.bin` and parses it using a high-performance C extension loaded via `ctypes` (`libfastparse.so`). Somewhere in `data.bin`, there is a malformed sequence of bytes causing the C extension to perform an illegal memory access and crash. 

Your objectives to resolve this incident:

1. **Diagnosis & Tracing**: The service crashes silently before finishing. Trace the system calls or analyze the intermediate state of `report_generator.py` to determine approximately where in the data stream the crash occurs.
2. **Fuzz Testing**: Write a Python fuzzer at `/home/user/fuzzer.py` that interfaces with `libfastparse.so`'s `parse_record(const char* data, int len)` function to isolate the exact 4-byte sequence that triggers the segmentation fault.
3. **MRE Creation**: Write a minimal reproducible example at `/home/user/mre.py`. This script should simply load the library, pass the exact 4-byte crashing sequence to `parse_record`, and demonstrably trigger the segfault.
4. **Identify Root Cause**: Once you find the 4-byte sequence, save it in hexadecimal format (e.g., `A1 B2 C3 D4`) to `/home/user/bad_signature.txt`.
5. **Mitigation**: Create a patched wrapper script at `/home/user/safe_report_generator.py`. This script must act identical to `report_generator.py`, but it must sanitize the input by explicitly filtering out/removing the 4-byte crashing sequence before passing the chunks to the C library. 
6. **Verification**: Run your `/home/user/safe_report_generator.py`. If successful, it will process the entirety of `data.bin` without crashing and write a file `/home/user/app/processed.log` containing the number of successfully parsed chunks.

**Environment details**:
* Working directory: `/home/user/app/`
* C library: `/home/user/app/libfastparse.so`
* Crashing script: `/home/user/app/report_generator.py`
* Input data: `/home/user/app/data.bin`

You have full access to standard Linux utilities (`strace`, `gdb`, `python3`, etc.). Solve the problem and ensure `processed.log` is successfully generated.