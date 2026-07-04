You are a security engineer tasked with automating the rotation of API credentials and implementing a strict filtering mechanism for credential rotation requests. The legacy system has been receiving malicious payloads, and you need to deploy a Bash-based filter to reject them.

We have provided a scanned memo containing the Q4 master rotation key. The image is located at `/app/rotation_memo.png`. You will need to extract the master key from this image (tesseract is installed and available).

Credential rotation requests are submitted as JSON files with the following structure:
```json
{
  "user": "alice",
  "nonce": "1a2b3c4d5e6f",
  "hmac": "a1b2c3d4..."
}
```

Your objective is to write a Bash script at `/home/user/payload_filter.sh` that validates these JSON payloads. The script must take exactly one argument: the path to the JSON file to be tested.

The script must implement the following security checks:
1. **Input Validation (Vulnerability Scanning):** The `user` field must NOT contain any shell metacharacters or command injection payloads. Specifically, reject any payload where the `user` field contains any of the following characters: `;`, `|`, `&`, `$`, `>`, `<`, `` ` ``.
2. **Cryptographic Integrity Verification:** The `hmac` field contains an HMAC-SHA256 hex digest. You must verify this signature. The HMAC is computed over the string `user:nonce` (e.g., `alice:1a2b3c4d5e6f`) using the master rotation key extracted from `/app/rotation_memo.png`. 

If the payload is entirely valid (safe `user` field AND a perfectly matching HMAC), your script must exit with a status code of `0`.
If the payload fails *any* of the security checks (invalid characters, mismatched HMAC, or missing fields), your script must print an error message to stderr and exit with a status code of `1`.

To help you develop and test your script, we have provided a corpus of payloads:
- `/app/corpus/clean/`: Contains perfectly valid, mathematically sound payloads. Your script MUST accept all of these (exit 0).
- `/app/corpus/evil/`: Contains adversarial payloads. These include files with forged HMACs (simulating a differential cryptanalysis attack on the token state) and payloads containing malicious shell injection attempts. Your script MUST reject all of these (exit 1).

**Deliverable:**
Write your final validation script to `/home/user/payload_filter.sh`. Ensure it is executable (`chmod +x`). 

Do not rely on external services; everything you need is local to the system. You may use standard Linux utilities like `jq`, `openssl`, `grep`, etc.