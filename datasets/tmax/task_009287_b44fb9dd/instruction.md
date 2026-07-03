You are a security researcher analyzing a suspicious Python script used by malware to parse proprietary binary payloads. You've intercepted a large binary payload that causes the parsing script to crash with a specific exception. 

Your task is to trace this crash, isolate the root cause, and minimize the payload to the absolute smallest byte sequence that still triggers the exact same failure.

**Environment details:**
- The parser script is located at `/home/user/parser.py`.
- The intercepted binary payload is located at `/home/user/suspicious.bin`.

**Your objectives:**
1. **Trace the Crash:** Run `/home/user/parser.py /home/user/suspicious.bin` and observe the crash. It should crash with `struct.error: unpack requires a buffer of 8 bytes` during an attempt to unpack a double (`<d`).
2. **Delta Debugging / Minimization:** Systematically reduce the size of the binary payload (using whatever scripting or manual techniques you prefer) to find the *absolute minimal file* that still triggers this exact crash (same exception, same line of code).
3. **Save Minimal Example:** Save your minimized payload to `/home/user/minimal_crash.bin`.
4. **Report:** Create a file at `/home/user/crash_info.txt` containing only the exact size in bytes of your `minimal_crash.bin` file (e.g., if the file is 42 bytes, the text file should contain exactly `42`).

**Constraints:**
- The original script `/home/user/parser.py` must NOT be modified.
- The `minimal_crash.bin` must be structurally valid enough to bypass the initial checks in the parser and reach the exact same vulnerability.
- Ensure `/home/user/crash_info.txt` contains only the numeric byte length.