You are a forensics analyst investigating a compromised host. The attacker exfiltrated sensitive data and left an encrypted payload behind, along with an intercepted audio recording.

Here are the details of the artifacts located in the `/app/evidence/` directory:
1. `/app/evidence/voicemail.wav` - An intercepted audio file containing a spoken hint about the encryption passphrase. You will need to transcribe this audio to find the hint. The hint specifies a word followed by a 4-digit PIN.
2. `/app/evidence/payload.enc` - The exfiltrated data, encrypted using OpenSSL AES-256-CBC with PBKDF2.

Your objectives:
1. **Analyze the Audio & Brute-Force the Key:** Transcribe the audio file to get the passphrase prefix. Write a script (bash or Rust) to brute-force the 4-digit suffix and decrypt `payload.enc`.
2. **Analyze the Payload:** The decrypted payload is a JSON file containing an array of objects representing compromised user accounts. Each object has the fields: `id`, `username`, `ssn` (Social Security Number), and `private_ssh_key`.
3. **Redact Sensitive Data:** You must redact the sensitive PII and credentials. Replace the value of every `ssn` field with the exact string `REDACTED_SSN` and every `private_ssh_key` field with the exact string `REDACTED_KEY`.
4. **Expose Securely via REST API (Rust):**
   Create a new Rust project in `/home/user/forensics_api`. Write an HTTP web server in Rust (using any framework you prefer, such as `axum`, `actix-web`, or standard library) that:
   - Listens on exactly `127.0.0.1:8181`.
   - Exposes a `GET /recovered-data` endpoint that returns the redacted JSON array.
   - Protects the endpoint with a Bearer token. The server must reject requests that do not have the header `Authorization: Bearer forensics-auth-token` with a 401 Unauthorized status.
5. Compile and start your Rust server in the background so it is ready to receive requests. Leave it running.