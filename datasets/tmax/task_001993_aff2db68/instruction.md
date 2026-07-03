You are a DevSecOps engineer tasked with enforcing a new "Policy as Code" standard to mitigate an open redirect vulnerability in a legacy login flow. 

The legacy system uses a custom, weak cryptographic token stored in an HTTP cookie (`redirect_token`) to determine where to send users after login. We are replacing the proprietary compiled binary with a Python-based enforcement script, but it must remain strictly backward-compatible with the existing token generation until the migration is complete.

Here is what you need to do:

1. **Recover the Encryption Key**: The original developer left the company, but left a voicemail containing the 6-digit numeric encryption key used for the tokens. The audio file is located at `/app/voicemail.wav`. You must transcribe this audio to recover the key.
2. **Analyze the Oracle**: We have provided the legacy compiled binary at `/app/token_oracle`. This binary takes exactly one argument: a raw HTTP Cookie header string (e.g., `Cookie: session=123; redirect_token=0a1b2c;`). 
3. **Implement the Policy Enforcer**: Write a Python script at `/home/user/policy_enforcer.py` that takes the HTTP Cookie string as its first command-line argument (`sys.argv[1]`). Your script must perfectly replicate the output of `/app/token_oracle` for any given input. 

**Requirements for `/home/user/policy_enforcer.py`**:
* Inspect the HTTP cookie string and extract the `redirect_token` value.
* Decrypt the token. (Hint: The legacy binary uses a simple repeating XOR cipher against the ascii representation of the 6-digit key from the audio file, followed by hex decoding/encoding).
* Enforce the redirect policy: The oracle only allows URLs that begin exactly with `https://trusted.corp.local/`.
* Output exactly what the oracle outputs (e.g., `ALLOW: <url>`, `DENY: Open Redirect`, `ERROR: Missing token`, or `ERROR: Invalid hex`).
* Your script must be strictly bit-exact in its standard output compared to the oracle across all edge cases (missing headers, malformed hex, invalid domains, etc.).

An automated fuzzer will test your Python script against the compiled oracle with thousands of random inputs to ensure 100% equivalence before we deploy it to production.