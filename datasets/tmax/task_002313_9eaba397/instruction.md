You are an incident responder investigating a recent security breach. We suspect the attacker exploited a vulnerability in our custom JWT implementation to bypass authentication and inject a malicious payload into our system.

We have gathered some evidence for you:
1. `/home/user/access.log`: An excerpt of our web server logs containing several suspicious HTTP requests with JWTs in the `Authorization: Bearer` headers.
2. `/home/user/app_config.json`: The application's configuration file containing the XOR secret key used for encrypting specific payload fields.

Your tasks are to:
1. Analyze the JWTs found in `/home/user/access.log`.
2. Identify the malicious token that bypasses signature validation by exploiting the `alg: none` vulnerability (the header will explicitly specify "none" as the algorithm).
3. Extract the `encrypted_data` field from the JSON payload of that specific token.
4. The `encrypted_data` is a Base64-encoded string. Once decoded, it was encrypted using a repeating-key XOR cipher. The key is stored in the `xor_key` field of `/home/user/app_config.json`.
5. Write a script to decrypt the data.
6. The decrypted data contains an injected cross-site scripting (XSS) payload. Save this exact decrypted plaintext string into a new file located at `/home/user/incident_report.txt`.

Ensure the final decrypted payload is written exactly as-is to `/home/user/incident_report.txt` with no surrounding whitespace or newlines.