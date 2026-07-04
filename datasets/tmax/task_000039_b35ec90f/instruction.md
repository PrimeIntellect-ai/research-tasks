You are a penetration tester tasked with analyzing a vulnerable custom authentication service and replicating its token generation logic for further fuzzing and intrusion detection testing.

We have captured an image of a handwritten note from the original developer at `/app/dev_note.png`. This image contains a specific TLS certificate pin (a 16-character alphanumeric string) and a secret salt used in the authentication flow.

Your objective is to:
1. Read the image at `/app/dev_note.png` and extract the TLS pin and the secret salt.
2. Write a Python script at `/home/user/auth_gen.py` that takes two command-line arguments: a username and a password.
3. The script must output a JSON object containing the simulated authentication token. The token generation algorithm is as follows:
   - Concatenate the extracted TLS pin, the username, the password, and the secret salt.
   - Compute the SHA-256 hash of this concatenated string.
   - Format the output exactly as `{"username": "<username>", "token": "<sha256_hash>"}`.
   - If the username contains any path traversal characters (`../` or `..\\`), the script should immediately output `{"error": "invalid username"}` and exit.

We have a stripped reference binary of the token generator at `/app/ref_auth_gen`. Your Python script must produce the exact same output as this reference binary for any given valid or invalid input. 

Please write the `/home/user/auth_gen.py` script.