You are a DevSecOps engineer tasked with implementing policy-as-code to prevent malicious deployments in our CI/CD pipeline. We recently suffered a breach, and the attacker left behind a taunting video artifact and several compromised compiled Python payloads.

Your task consists of three phases:

**Phase 1: Video Forensics (Payload Identification)**
The attacker uploaded a video to `/app/breach_record.mp4`. We suspect this video steganographically encodes the core signature of their exploit payload.
- The video consists of exactly 64 frames.
- Each frame is either completely black or completely white.
- Calculate the average luminance of each frame. A bright frame (average pixel value > 128) represents a binary `1`, and a dark frame (average pixel value < 128) represents a binary `0`.
- Group the bits into 8-bit bytes (Most Significant Bit first) to decode an 8-character ASCII string. This string is the "Malware Signature".

**Phase 2: Policy Checker Creation (Reverse Engineering & Integrity)**
Write a Python script at `/home/user/policy_checker.py` that will act as our automated CI/CD gatekeeper. The script must take a single command-line argument: the path to a compiled Python bytecode file (`.pyc`).

For each file evaluated, your script must perform the following checks:
1. **Integrity Check:** Compute the SHA256 hash of the `.pyc` file. Verify if this hash exists anywhere in the authorized manifest file located at `/app/manifest.txt`. If the hash is NOT in the manifest, the file violates policy.
2. **Bytecode Reverse Engineering:** If the file is in the manifest, you must dynamically load and disassemble its code object (e.g., using `marshal` and the `dis` or `types` modules). You must determine if the "Malware Signature" (decoded in Phase 1) is present in the bytecode's constants. *Note: The attacker obfuscates the payload by splitting the signature into two smaller string constants that are concatenated at runtime (e.g., using `BINARY_ADD`). Your analyzer must detect if the signature exists either as a whole string or can be formed by combining adjacent string constants in the code object.*

**Phase 3: Enforcement**
Your script must output to standard out and exit with specific status codes:
- Exit with status code `0` (Clean) ONLY if the file's hash is in the manifest AND the malware signature is nowhere to be found in its constants.
- Exit with status code `1` (Evil/Rejected) if the file's hash is missing from the manifest OR the malware signature is detected in the bytecode.

To test your script, we have provided two corpora of `.pyc` files:
- `/app/clean_corpus/`: Contains policy-compliant binaries.
- `/app/evil_corpus/`: Contains binaries harboring the payload or lacking integrity.

Your script will be programmatically tested against both corpora.