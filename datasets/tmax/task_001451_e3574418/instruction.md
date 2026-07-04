You are an incident responder dealing with an active attack on a file upload handler. The attackers are using a custom obfuscation tool to hide path traversal and XSS payloads in the upload paths, bypassing your current WAF. 

We recovered the attackers' decoding utility, which is available as a stripped binary at `/app/decode_payload`. 
However, the tool is protected by a 4-digit PIN. If you run `/app/decode_payload <PIN> <obfuscated_string>`, it will output the plaintext payload if the PIN is correct, or "Access Denied" if the PIN is incorrect. 

Your task is to write a bash script at `/home/user/filter_uploads.sh` that acts as a new WAF filter. 
The script must:
1. Read a single obfuscated string from Standard Input (STDIN).
2. Decode the string using the `/app/decode_payload` binary. (You will need to brute-force or figure out the 4-digit PIN first and include it in your script).
3. Analyze the decoded plaintext.
4. Output exactly `REJECT` (and nothing else) if the decoded payload contains evidence of a Path Traversal attack (e.g., `../`, `..%2f`, `%2e%2e%2f`) OR an XSS attack (e.g., `<script>`, `onerror=`, `javascript:`).
5. Output exactly `ACCEPT` (and nothing else) if the decoded payload is a safe file path (e.g., `images/pic.png`, `document.pdf`) and contains no malicious patterns.

Requirements:
- Your script must be written entirely in Bash.
- It must handle STDIN properly.
- Ensure no extraneous output (like the brute-forced PIN or the plaintext payload) is printed to STDOUT, as automated grading will strictly check for `ACCEPT` or `REJECT`.

To test your script, you can assume there are malicious and benign obfuscated payloads in the wild, but you must construct your logic to catch common path traversal and XSS primitives.