You are a penetration tester analyzing a proprietary system. You have discovered a stripped binary located at `/app/payload_gen`. The target system uses this binary to transform file integrity checksums (SHA-256 hashes) into specialized network payloads to bypass internal firewall restrictions. 

To proceed with your vulnerability scanning framework, you need a native Python implementation of this payload generation algorithm.

Your task is to:
1. Reverse engineer the stripped binary `/app/payload_gen`.
2. Write a Python script at `/home/user/payload_gen.py` that exactly replicates the binary's behavior.
3. Your Python script must accept a single command-line argument: a 64-character hex string (representing a SHA-256 hash).
4. Your script must print the transformed hex string to standard output, exactly matching the output of `/app/payload_gen` for the same input.

Ensure your Python script is executable and operates cleanly without extra debug output. Automated verifiers will test your script against the original binary using thousands of randomly generated 64-character hex strings to ensure bit-exact equivalence.