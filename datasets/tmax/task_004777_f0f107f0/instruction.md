You are a forensics analyst recovering encrypted evidence from a compromised Linux host. The attackers used a custom exfiltration mechanism, and you need to build a secure, isolated tool to decode the intercepted traffic.

**Part 1: Fix the Sandbox Policy Enforcer**
For safety, our forensic environment requires all payload decoding to run inside a sandboxed process. We use a proprietary tool called `sandbox-runner`. 
1. The source code for `sandbox-runner` v1.2.0 is vendored at `/app/sandbox-runner-1.2.0`. 
2. However, the package was modified by the attackers to prevent compilation. It currently fails to build via `make`. 
3. Diagnose the compilation failure (it is a trivial perturbation in the `Makefile` and C source involving strict warnings) and fix it.
4. Run `make` and place the compiled `sandbox-runner` executable in `/usr/local/bin/`.

**Part 2: Malware Decoder Implementation**
We recovered a stripped, binary version of the attacker's decoder at `/app/oracle/malware_decoder`. By reverse engineering it, we found:
1. It reads encrypted payload bytes from standard input (`stdin`) and writes the decrypted bytes to standard output (`stdout`).
2. The encryption is standard AES-128-CTR.
3. The 16-byte AES key is the MD5 hash of the ASCII string `"EXFIL_FORENSICS_2024"`.
4. The first 16 bytes of the input stream constitute the CTR nonce (initial counter block). The rest of the stream is the ciphertext.

You must implement a pure Python version of this decoder to run securely in our environment.
1. Create a script at `/home/user/decode_trace.py`.
2. The script must read standard input until EOF, decrypt the stream using the above cryptography parameters, and write the raw decrypted bytes to standard output.
3. Your script must perfectly match the bit-for-bit behavior of the `/app/oracle/malware_decoder` binary for any arbitrary input stream of length >= 16 bytes.
4. Ensure your script is efficient and handles binary I/O correctly without encoding issues (use `sys.stdin.buffer` and `sys.stdout.buffer`).

Once you have verified your script works and the sandbox-runner compiles, you are finished. The automated system will test your Python implementation by fuzzing it against the binary oracle.