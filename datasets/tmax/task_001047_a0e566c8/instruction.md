You are a network security engineer investigating a breach. An attacker exploited an open redirect vulnerability in the company's login flow to steal session tokens. 

We have provided you with:
1. A vendored copy of the company's proprietary session library at `/app/custom_session_lib`. Unfortunately, a junior developer broke the package configuration, so it currently fails to install.
2. A snippet of intercepted HTTP traffic in `/home/user/traffic.txt` showing the attacker exploiting the open redirect to steal a token. The stolen token belonged to a guest user: `username:guest_user,role:guest`.

Your objectives are:
1. **Fix and Install the Library**: Identify and fix the deliberate perturbation in `/app/custom_session_lib` (look closely at the package configuration/setup files) and install it in the current Python environment.
2. **Cryptanalysis & Decoding**: The library uses a weak repeating-key XOR stream cipher for payload encoding, followed by a hex encoding. Using the intercepted token from `/home/user/traffic.txt` and your knowledge of the plaintext (`username:guest_user,role:guest`), recover the secret encryption key.
3. **Payload Forgery**: Write a Python script at `/home/user/forge.py` that takes a single username as a command-line argument and prints out a valid, hex-encoded admin session token for that user. The plaintext format must be exactly `username:<arg>,role:admin`.
4. **Sandboxed Validation**: Since the legacy decryption library is unsafe and prone to memory corruption on malformed inputs, your `forge.py` script must safely verify the generated token by calling the library's verification function (`custom_session_lib.verify_token(token)`) in a strictly isolated child process (e.g., using the `subprocess` module) before printing it to standard output. If the validation fails or crashes, `forge.py` should exit with a non-zero status.

Your script will be tested against a hidden suite of 50 usernames. To pass, it must achieve a perfect success rate in forging and validating admin tokens. 

Ensure your final script only prints the hex-encoded token to standard output, with no other text.