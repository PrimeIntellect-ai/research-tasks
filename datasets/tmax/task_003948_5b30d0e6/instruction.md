You are a network engineer tasked with restoring and inspecting a broken traffic monitoring pipeline. The system consists of a frontend reverse proxy (Nginx) and a backend Python Flask token-generation service. Additionally, you must replace an old compiled legacy binary used for inspecting captured secure tokens with a new Python script.

Part 1: Service Composition
Two user-space services are prepared in your home directory but are misconfigured:
1. Nginx (Frontend): Configured to run on port 8080 using the config at `/home/user/proxy/nginx.conf`.
2. Flask App (Backend): Runs on port 5000. Its source is at `/home/user/backend/app.py`.

Your tasks for the services:
- Edit `/home/user/proxy/nginx.conf` so that any request to the path `/inspect` is proxied to the backend at `http://127.0.0.1:5000`.
- The backend service requires an environment variable to securely generate tokens. Create a file at `/home/user/backend/.env` containing exactly: `AUTH_KEY=AlphaBravo123`
- Ensure both services are running and test the end-to-end flow. When correctly configured, running `curl http://127.0.0.1:8080/inspect` should return a successful JSON response containing a test token. Set the permissions of `/home/user/backend/.env` to `600` so only the owner can read it.

Part 2: Token Parser Replacement
We have a legacy compiled binary located at `/app/legacy_parser`. It takes a single base64-encoded token as a command-line argument, decrypts it, and prints the result. We lost the source code and need you to write a drop-in replacement in Python at `/home/user/parse_token.py`.

The parsing algorithm works as follows:
1. Accept exactly one command-line argument (the token string).
2. Attempt to Base64-decode the argument. If decoding fails, print `ERROR: INVALID_B64` and exit with code 1.
3. The decoded bytes must start with the exact 4-byte header `b'NET:'`. If it does not, print `ERROR: BAD_HEADER` and exit with code 2.
4. Extract the payload (everything after the first 4 bytes).
5. Decrypt the payload by applying a bitwise XOR operation with the hexadecimal value `0x5C` against every byte.
6. Print the decrypted payload as a lowercase hexadecimal string (e.g., `deadbeef`) to standard output and exit with code 0.

Your Python script must behave BIT-EXACTLY like `/app/legacy_parser` for any possible input. It will be aggressively fuzzed against the legacy binary to ensure perfect equivalence.