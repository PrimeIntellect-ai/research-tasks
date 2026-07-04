We are migrating our legacy web backend from Python 2 to Python 3. Our system uses a custom binary serialization format for session tokens, which are processed by a legacy C extension. Recently, we discovered that malicious tokens can crash this binary, causing denial-of-service or potential remote code execution. 

To mitigate this while we rewrite the entire backend, we need a pure Python 3 pre-filter that analyzes the raw hex-encoded tokens and drops malicious ones before they ever reach the C level via FFI.

We have extracted the standalone stripped binary at `/app/legacy_decoder`. It reads a single hex-encoded token from standard input and prints the parsed JSON. 
We also captured samples of traffic:
- `/app/corpus/clean/`: Contains 50 `.txt` files with legitimate, safe hex-encoded tokens.
- `/app/corpus/evil/`: Contains 50 `.txt` files with malicious tokens that exploit memory corruption flaws in the legacy decoder.

Your task:
1. Analyze the binary and the provided corpora to understand the token format and the exact conditions that cause the legacy C decoder to crash (segmentation faults, out-of-bounds reads, or buffer overflows).
2. Write a Python 3 script at `/home/user/prefilter.py` that implements a safe parser and validator for these tokens.
3. The script must take exactly one command-line argument: the hex-encoded token string.
   Usage: `python3 /home/user/prefilter.py <hex_string>`
4. If the token is perfectly valid and safe to process, the script must exit with status code `0`.
5. If the token violates the structural integrity of the format or triggers the known buffer overflow conditions, the script must exit with status code `1`.

Your script must accurately classify 100% of the provided clean and evil tokens without relying on `subprocess` to call the legacy binary (we cannot afford the overhead or the risk of crashing in production). You should reverse-engineer the serialization format and the vulnerability constraints by observing the crashes in `/app/legacy_decoder` using standard memory debugging tools (like `gdb` or `valgrind`) and by analyzing the corpora.