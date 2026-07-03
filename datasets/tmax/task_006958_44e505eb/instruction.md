You are an incident responder investigating a compromised Linux server. We suspect an attacker authenticated via SSH, added their key to the `authorized_keys` file for persistence, and then sent a malicious payload to our internal sandbox application. 

You have been provided with two files:
1. `/home/user/incident/server.log`: A custom consolidated log file containing both SSH login events and application requests.
2. `/home/user/incident/authorized_keys`: The compromised SSH authorized_keys file.

Your task is to:
1. Write a Rust program (`/home/user/investigator.rs`) that parses `/home/user/incident/server.log`. 
2. Identify the attacker's IP address. The attacker is the user who sent an application request (`APP_REQ`) where the hex-encoded `PAYLOAD` field, when decoded to an ASCII string, contains the substring `evil.com`.
3. Correlate this IP address with the `SSH_LOGIN` events in the log to find the attacker's SSH key fingerprint (SHA256).
4. Remove the attacker's SSH key from `/home/user/incident/authorized_keys`. You must match the SHA256 fingerprint found in the log to the actual base64 key in the `authorized_keys` file (Note: You may need to compute the SHA256 fingerprint of the keys in `authorized_keys` to find the match. Standard SSH fingerprints are unpadded base64 of the SHA256 hash of the decoded public key bytes).
5. Generate a report in JSON format at `/home/user/report.json` containing the findings. The JSON must have the following exact schema:
```json
{
  "attacker_ip": "x.x.x.x",
  "decoded_payload": "the full decoded ascii string",
  "compromised_fingerprint": "SHA256:..."
}
```

Constraints:
- Use Rust to write the correlation and analysis logic. You can use standard tools (`ssh-keygen`, `grep`, `awk`) in combination with your Rust script, but the core hex decoding and log correlation must be done in Rust.
- Make sure to overwrite `/home/user/incident/authorized_keys` with the malicious key completely removed. Do not alter the remaining keys.