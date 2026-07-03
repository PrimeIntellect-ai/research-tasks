You are a mobile build engineer maintaining a lightweight CI pipeline. To reduce container sizes and remove Python dependencies from our base build runners, we need to rewrite some of our pipeline utilities into pure Bash (with standalone binaries where necessary).

One of these utilities is responsible for communicating with our internal signing server via WebSockets. It calculates a checksum of the artifact name to ensure integrity, sends a JSON payload, and extracts the resulting signature.

The original Python script is located at `/home/user/legacy_sign.py`.
A mock version of the signing server for testing is provided at `/home/user/ws_server.py`.

Your task:
1. Start the mock WebSocket server. You may need to run `pip install --user websockets` first. The server will listen on `ws://127.0.0.1:8765`.
2. Translate the logic of `legacy_sign.py` into a Bash script located at `/home/user/ci_sign.sh`.
3. Your Bash script must accept the artifact name as the first argument (`$1`).
4. To handle the WebSocket communication in Bash without root access, download the standalone `websocat` binary to `/home/user/websocat` and make it executable (e.g., `wget https://github.com/vi/websocat/releases/latest/download/websocat.x86_64-unknown-linux-musl -O /home/user/websocat`).
5. Your Bash script should construct the JSON payload (including the correct SHA-256 checksum of the artifact name without a trailing newline), send it to the WebSocket server using your local `websocat`, and parse the signature from the JSON response.
6. Run your completed `/home/user/ci_sign.sh` script with the argument `mobile-release-v2.1.apk`.
7. Save *only* the extracted signature string to `/home/user/signature.txt`.

Ensure your Bash script makes the correct payload and processes the response accurately, maintaining the exact same logic as the Python script.