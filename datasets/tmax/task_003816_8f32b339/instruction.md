You are an infrastructure engineer automating a deployment provisioning system. We are implementing a "Voice-Ops" gateway where emergency deployment rollouts are authorized via an audio message.

Your objective is to complete the following multi-stage setup:

1. **Extract Authorization Token:**
   There is an audio file located at `/app/auth_message.wav`. You must transcribe this audio file to retrieve the secret deployment passcode. You can assume `whisper-cli` or similar audio processing tools are available, or you may write a script to extract the embedded text track/metadata if it's stored there. The spoken sentence ends with a 6-digit passcode.

2. **Develop the Deployment Gateway (Go):**
   Write a Go application at `/home/user/deploy_gateway.go` and run it. The application must:
   - Listen on `127.0.0.1:8080`.
   - Expose an HTTP POST endpoint at `/deploy`.
   - Require an `X-Voice-Auth` header. The value must exactly match the 6-digit passcode transcribed from the audio file.
   - If the header is missing or incorrect, return HTTP 401 Unauthorized.
   - If the header is correct, the Go application must execute a bash script located at `/home/user/rollout.sh` and return HTTP 200 OK.

3. **Develop the Rolling Deployment Script (Bash):**
   Write a robust bash script at `/home/user/rollout.sh` that simulates a rolling deployment.
   - The script must read a list of target servers from `/app/servers.txt` (format: one IP address per line).
   - Use `awk`, `sed`, or `grep` to filter out any lines starting with `#` or empty lines.
   - For each valid IP address, append the line `DEPLOYED TO: <IP>` to `/home/user/deploy_log.txt`.
   - Include error handling: if `/app/servers.txt` does not exist, the script should exit with code 1 and write `ERROR: servers.txt missing` to `/home/user/deploy_log.txt`.
   - Ensure the script is executable.

Ensure your Go server is compiled and running in the background listening on the required port.