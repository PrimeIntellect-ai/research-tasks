Wake up, we have a critical 3 AM incident. 

Our legacy telemetry ingest pipeline has started failing across multiple nodes. The issue stems from a proprietary data encoder, `telemetry_obfuscator`, which runs on edge devices to pack and obfuscate memory dumps before transmission. We need to deploy a pure Python equivalent immediately to our new ARM fleet, but the original C source code was lost years ago by a former contractor.

All we have is the compiled, stripped x86_64 binary located at `/app/telemetry_obfuscator`. 

Your task is to reverse-engineer the exact behavior of this stripped binary and write a fully functionally equivalent Python script at `/home/user/py_obfuscator.py`. 

The Python script must:
1. Read raw binary data from standard input (`stdin`).
2. Apply the exact same encoding/obfuscation algorithm as the original C binary.
3. Write the obfuscated binary data to standard output (`stdout`).

You will need to analyze the binary (e.g., using `gdb`, `objdump`, `strace`, or `ltrace`), extract any hardcoded keys or strings, trace its intermediate state to understand the block transformation math, and carefully handle its padding and boundary conditions. Be warned: the original author was known for off-by-one errors and unusual padding logic for inputs that aren't perfectly aligned to the block size. 

The automated verification will fuzz your script against the original binary using thousands of random binary inputs of varying lengths (0 to 2048 bytes) to ensure bit-for-bit equivalence in the output.

Write your solution to `/home/user/py_obfuscator.py`. Do not include any hardcoded test inputs in the final script—it should act purely as a UNIX filter (stdin to stdout).