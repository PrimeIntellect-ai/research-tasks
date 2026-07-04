You are tasked with resolving a service outage and deploying a secure internal API backend. The previous administrator left behind a partially configured setup that currently returns a 502 Bad Gateway.

Here is the situation:
1. **Audio Decoding**: There is an audio file at `/app/voicemail.wav`. This file contains a sequence of DTMF tones representing an emergency override PIN. You need to decode this PIN (a sequence of digits).
2. **Go Backend**: Write a Go web server at `/home/user/app/backend.go` and compile it. The server must listen on a UNIX socket at `/tmp/backend.sock`. It should expose an HTTP GET endpoint at `/pin` that returns a JSON response containing the PIN you decoded, in the exact format: `{"status": "ok", "pin": "YOUR_DECODED_PIN"}`.
3. **Process Supervision**: The Go backend must be highly available. Write a bash supervisor script at `/home/user/keepalive.sh` that checks if your compiled Go server is running, and starts it in the background if it is not. Configure the current user's `crontab` to run this script every minute. 
4. **Fixing the Reverse Proxy**: There is a user-mode Nginx instance configured at `/home/user/nginx/nginx.conf`. It is currently listening on `127.0.0.1:8080` but returns a 502 error when accessing `/pin` because its upstream `proxy_pass` directive points to a non-existent socket. Fix the configuration to point to your Go backend's socket, and reload/restart the Nginx process.
5. **SSH Tunneling**: External access to port 8080 is blocked by a local firewall. To expose the API to the external verifier, you must set up a local port forward using SSH. Establish a background SSH tunnel that listens on `0.0.0.0:8888` and forwards traffic to `127.0.0.1:8080`. You will need to configure SSH key-based authentication for the `user` account to `localhost` so the tunnel can be established without password prompts.

Ensure the final state satisfies the following:
- Nginx is running and proxying requests.
- The SSH tunnel is active and listening on port 8888.
- An HTTP GET request to `http://127.0.0.1:8888/pin` successfully returns the JSON payload with the decoded DTMF PIN.