You are acting as a penetration tester and security engineer. We have intercepted a large batch of JSON Web Tokens (JWTs) from a target's network. We suspect the target's internal API gateways have a misconfigured Firewall/WAF that fails to enforce strict Content Security Policies, allowing malicious tokens to pass through. 

Specifically, we suspect the tokens are vulnerable to the classic `alg=none` attack (where the signature algorithm is set to `none`, `None`, `NONE`, etc., and the signature is stripped), OR they contain a specific backdoor subject (`sub`) claim that the attackers are using to bypass network policies.

We have an intercepted audio snippet from the attackers detailing the exact backdoor subject claim they use. The audio file is located at `/app/intercepted_comms.wav`. 

Your task is to write a Python CLI tool that acts as a vulnerability scanner and intrusion detection filter for these JWTs.

Create a script at `/home/user/jwt_analyzer.py` that takes a single file path as an argument. The file will contain a single raw JWT string.
The script must:
1. Decode the JWT header and payload (without verifying the signature, as this is a scanner meant to detect structurally malicious payloads before signature validation).
2. Detect if the token is using the `alg=none` vulnerability (case-insensitive check for "none" in the `alg` header).
3. Detect if the token's payload contains the specific backdoor subject (`sub`) claim spoken in `/app/intercepted_comms.wav`.
4. Exit with status code `1` (rejected/vulnerable) if either the `alg=none` vulnerability OR the backdoor claim is present.
5. Exit with status code `0` (clean/secure) if the token is structurally sound (e.g., `alg` is `HS256`, `RS256`, etc.) and does not contain the backdoor claim.

Example invocation:
`python3 /home/user/jwt_analyzer.py token.txt`

You may use any standard transcription tool (like `whisper` or `ffmpeg` to listen/convert) to analyze the audio file. Ensure your script handles base64url decoding properly, including adding necessary padding.