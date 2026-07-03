You are an incident responder investigating a suspected breach on a web server. We believe an attacker exploited an open redirect vulnerability in the login flow to exfiltrate an authentication token, which they then used to forge an administrator session.

We have collected the server's access logs and the source code for the custom token generation library.

You are provided with the following files:
1. `/home/user/access.log`: The web server access logs containing normal traffic and the suspected open redirect attack.
2. `/home/user/auth_lib.rs`: The Rust source code of the authentication library used by the server, which contains a proprietary (and likely flawed) token encoding scheme.

Your objectives:
1. Parse the security logs in `/home/user/access.log` to identify the malicious HTTP request. Look for a request that redirects to an external, unrecognized domain (`evil-attacker.com`) and extracts a token parameter.
2. Analyze the `auth_lib.rs` code to reverse-engineer how the server encodes authentication tokens.
3. Write a Rust program at `/home/user/investigate.rs` that reads the token from the log, implements the inverse of the token encoding algorithm (cryptanalysis / decoding), and extracts the plaintext JSON payload.
4. Run your Rust script and output the decoded plaintext JSON payload exactly as it is to the file `/home/user/decoded_payload.txt`.

Ensure your Rust program can be compiled and executed using `rustc` or `cargo`. The final `/home/user/decoded_payload.txt` must contain only the decoded string without any surrounding whitespace or newlines not present in the original token payload.