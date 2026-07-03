You are acting as a security engineer tasked with rotating credentials for a legacy intrusion detection and logging service. The legacy system has been decommissioned, but we need to recover the original credentials from its audit logs to ensure they aren't reused in our new systems, and to test our new password validation rules against them.

In `/home/user/legacy_auth.log`, there is a dump of recent authentication logs. 
Some lines contain encoded payloads prefixed with `AUTH_PAYLOAD=`. These payloads are Base64 encoded.
When decoded, the valid authentication payloads follow the format: `username:md5_hash` (e.g., `admin:81dc9bdb52d04dc20036dbd8313ed055`). 
Note that the log file also contains noise, regular errors, and Base64 strings that do not follow this username:hash format after decoding. You must filter out the invalid ones using pattern matching.

We know from legacy documentation that all passwords for these accounts were strictly 4-digit PINs (e.g., "0000" to "9999").

Your task involves multiple phases:
1. Parse `/home/user/legacy_auth.log` to find and extract the `AUTH_PAYLOAD=` strings.
2. Decode the Base64 payloads and isolate the ones that perfectly match the `username:md5_hash` pattern. (The MD5 hash is always 32 hex characters).
3. Write a Python script to brute-force and crack the MD5 hashes to recover the original 4-digit PINs.
4. Output the results to a JSON file located exactly at `/home/user/cracked_creds.json`.

The output file `/home/user/cracked_creds.json` must be a flat JSON dictionary mapping the extracted usernames to their cracked 4-digit PINs as strings. 

Example output format:
```json
{
  "admin": "1234",
  "guest": "9999"
}
```

Please complete the extraction, decoding, cracking, and saving process. You may use Python and standard shell commands to accomplish this.