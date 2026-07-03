You are an incident responder tasked with investigating a potential breach on a Linux web server. The system administrators have contained the threat and provided you with a snapshot of the logs, but the logs were encrypted by the logging daemon before being exfiltrated. 

You have been provided with a workspace at `/home/user/incident_workspace`. 

Your investigation has the following phases:

**Phase 1: Decryption Tool Development (Rust)**
The logging daemon uses AES-256-GCM to encrypt log files. You need to write a Rust tool to decrypt them.
1. Create a new Rust project at `/home/user/decryptor`.
2. The encryption key and nonce are stored in hex format in `/home/user/incident_workspace/crypto_params.txt`. The first line is the 32-byte AES-256 key, and the second line is the 12-byte nonce.
3. Write a Rust program that reads these hex-encoded parameters and decrypts the two encrypted log files located at:
   - `/home/user/incident_workspace/encrypted/web.log.enc`
   - `/home/user/incident_workspace/encrypted/auth.log.enc`
   *Note: Use standard Rust cryptography crates like `aes-gcm` and `hex`. You may need to add them to your `Cargo.toml`.*
4. Your tool must write the plaintext logs to `/home/user/incident_workspace/decrypted/web.log` and `/home/user/incident_workspace/decrypted/auth.log`.

**Phase 2: Log Parsing and Correlation**
Once decrypted, you must analyze the logs using bash utilities to trace the attacker's actions.
1. Inspect `web.log` to identify the IP address of the attacker. The attacker exploited a command injection vulnerability in a specific web API endpoint.
2. Correlate the timestamp and the injected command from `web.log` with the privilege escalation events in `auth.log`.
3. Identify the exact system binary the attacker used to escalate privileges to `root` (e.g., abusing a misconfigured sudo permission).

**Phase 3: Reporting**
Generate a structured JSON report of your findings. Create a file at `/home/user/incident_report.json` with the following precise schema:

```json
{
  "attacker_ip": "<IP_ADDRESS_HERE>",
  "exploited_endpoint": "<PATH_OF_EXPLOITED_ENDPOINT_WITHOUT_QUERY_STRING>",
  "privesc_binary": "<FULL_PATH_TO_ABUSED_BINARY>"
}
```

**Constraints & Notes:**
- You do not have root access. You must use the provided workspace.
- The `crypto_params.txt` contains exactly two lines: the hex key and the hex nonce.
- The AES-GCM tag is appended to the end of the ciphertext in the `.enc` files (this is the standard behavior for the `aes-gcm` crate where ciphertext and tag are concatenated).