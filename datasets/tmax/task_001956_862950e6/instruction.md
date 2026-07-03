You are an incident responder investigating a recent breach of our internal analytics platform. The attackers managed to forge authentication tokens to bypass access controls.

We have recovered a screenshot taken by the attacker, located at `/app/evidence.png`. It contains a fragment of a leaked internal memo discussing a fallback mechanism used in our custom JWT implementation.

Your task is to:
1. Extract the text from `/app/evidence.png` (Tesseract OCR is available on the system).
2. Analyze the extracted text to understand the vulnerability or the leaked secret used by the attackers to forge tokens. 
3. Develop a Go-based intrusion detection filter. Write your source code to `/home/user/filter.go` and compile it to `/home/user/auth_filter`.
4. Your compiled binary `/home/user/auth_filter` must accept a single command-line argument representing the absolute path to a file containing a single authentication token.
   - If the token is cryptographically valid and clean, the program must exit with status code `0`.
   - If the token is forged (evil), exploits the vulnerability, or contains malicious path-traversal payloads in its claims, the program must exit with status code `1`.
5. The tokens are standard JWTs (JSON Web Tokens). You will need to implement pattern matching and cryptanalysis to identify the forged tokens (e.g., checking for the `none` algorithm bypass or verifying against the leaked secret).

The system contains a set of sample tokens you can use to test your program:
- Legitimate tokens are located in the directory `/app/clean_tokens/`
- Forged tokens found in the web server logs are located in `/app/evil_tokens/`

To succeed, your program must perfectly distinguish between the clean and evil tokens.