You are an incident responder investigating a suspected privilege escalation attack on a legacy API. The attackers have been forging authentication tokens to gain administrative access. 

During the investigation, you recovered a developer's voice memo detailing the cryptographic secret used for token generation, located at `/app/incident_audio.wav`. 

The system uses a custom authentication token format:
`[Base64URL_encoded_JSON_payload].[SHA256_hex_signature]`

The signature is computed as: `SHA256(Base64URL_encoded_JSON_payload + secret_key)`.

Valid tokens must meet the following criteria:
1. The signature must perfectly match the computed SHA256 hash.
2. The JSON payload must contain an `"exp"` (expiration) UNIX timestamp that is strictly greater than `1710000000`.
3. The `"user_id"` field must be strictly alphanumeric.
4. Any attempt at privilege escalation (e.g., token forging or invalid signatures) must be blocked. 

Your objective is to build a robust token validator that accepts legitimate tokens and blocks malicious/invalid ones.

Write a Python script at `/home/user/validator.py` that takes the path to a file containing a single token as its first command-line argument:
`python3 /home/user/validator.py <path_to_token_file>`

The script must:
- Print "VALID" to standard output and exit with code `0` if the token is completely valid and secure.
- Print "INVALID" to standard output and exit with code `1` if the token is expired, tampered with, has an invalid signature, or contains a malicious payload.

To aid your development, we have provided two directories of sample tokens:
- `/app/corpus/clean/` - Contains 50 legitimate tokens that your script MUST accept (exit code 0).
- `/app/corpus/evil/` - Contains 50 forged, expired, or malicious privilege-escalation tokens that your script MUST reject (exit code 1).

You will need to install any necessary tools to transcribe the audio file and recover the secret key before building your validator.