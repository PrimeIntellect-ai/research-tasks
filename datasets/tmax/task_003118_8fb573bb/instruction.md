You are a security engineer tasked with preparing for a critical credential rotation. Your organization relies on an old, undocumented authentication service that validates access tokens. Recently, attackers have discovered a cryptanalytic flaw (a differential vulnerability) in the custom cipher used by the service, allowing them to forge tokens that the service incorrectly accepts.

Your goal is to build a robust detection and filtering pipeline to identify these forged tokens before we rotate to the new system. 

Here are your resources and requirements:
1. **The Legacy Service (Stripped Binary):** Located at `/app/legacy_auth_service`. This stripped ELF binary takes a 32-character hex string (16 bytes) as a command-line argument and exits `0` if it thinks the token is valid, and `1` if invalid. It is highly vulnerable to buffer overflows, so it must not be run directly on untrusted input.
2. **The Corpora:** We have captured samples of tokens.
   - `/app/corpora/clean/`: Contains files, each with a single 32-character hex string of a genuinely generated, valid token.
   - `/app/corpora/evil/`: Contains files with forged tokens that exploit the differential vulnerability. The legacy binary incorrectly accepts these as valid.
3. **Sandboxing Requirement:** Write a bash script `/home/user/sandbox_test.sh` that takes a token string as an argument and safely executes `/app/legacy_auth_service <token>` using `bwrap` (bubblewrap). The sandbox must isolate the process: read-only access to `/`, no network access (`--unshare-all`), and drop privileges (run as a restricted user environment).
4. **The Detector (Python):** Write a Python script `/home/user/token_filter.py` that acts as an intrusion detection filter. It must take a 32-character hex token as its first command-line argument.
   - The script should analyze the token's cryptographic patterns to distinguish between "clean" and "evil" tokens. 
   - You will need to analyze the provided corpora to deduce the mathematical or pattern-based difference (the cryptanalytic differential) between the valid tokens and the forged ones.
   - If the token is forged (evil), print exactly `EVIL` to standard output.
   - If the token is valid (clean), print exactly `CLEAN` to standard output.

To succeed, you must reverse-engineer the flaw by analyzing the token patterns in the corpora, build the sandbox script, and implement the Python filter. Your `token_filter.py` will be tested against a hidden set of clean and evil tokens to verify it correctly identifies 100% of both sets.