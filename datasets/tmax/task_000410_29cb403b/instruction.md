We have a security incident involving our credential rotation system. An internal utility package, `cred-rotator`, was recently updated, but we suspect it has a deliberate perturbation that leaks credentials via command-line arguments, making them visible in system process lists and security logs.

Your task has two parts:

Part 1: Fix the Vendored Package
The source code for `cred-rotator` (version 1.2.0) is vendored at `/app/cred-rotator`. It contains a bug in how it executes a subprocess for key generation, passing the raw master password as a command-line argument rather than via environment variables or stdin. 
1. Analyze the package in `/app/cred-rotator`.
2. Find the vulnerability in `rotator/cli.py` where `subprocess.run` is called.
3. Modify the code to pass the `master_key` securely via an environment variable named `ROTATOR_MASTER_KEY` instead of as a command-line argument, ensuring the script `bin/generate_key.sh` still receives it correctly (you will need to update `bin/generate_key.sh` to read from the environment variable).

Part 2: Token Generation and Log Correlation
Our security monitoring system captures HTTP headers and cookies during the credential rotation process. We need a token generation script to validate requests based on a specific algorithm. 
We have a reference implementation (a stripped binary) at `/opt/oracles/token_oracle`.

Write a Python script at `/home/user/token_generator.py` that takes exactly two arguments:
1. `session_id` (a 16-character hex string)
2. `client_ip` (an IPv4 address)

The script must output a 64-character hex token to standard output. 
The algorithm used by the oracle is as follows:
- Concatenate `session_id`, the string `|`, and `client_ip`.
- Compute the SHA-256 hash of this string.
- XOR the first 16 bytes of the hash with the last 16 bytes of the hash.
- The output token is the hex representation of the original SHA-256 hash, but with the first 16 bytes replaced by the XOR result (total 32 bytes, which is 64 hex characters).

Your Python script's behavior must be bit-exact equivalent to the reference oracle for any valid input pair.

Write the script and ensure it is executable. Do not modify the oracle.