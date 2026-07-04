You are an infrastructure specialist managing a fleet of microservices. We are deploying a new Go-based network filtering daemon to analyze incoming traffic logs and drop malicious payloads before they reach our backend services.

Your manager left a voice memo detailing the exact criteria for what constitutes "malicious" network traffic in our current threat landscape. 
You need to accomplish the following:

1. **Analyze the Audio Instructions:**
   There is an audio file located at `/app/instructions.wav`. Use any available tool (e.g., `whisper` CLI, if installed, or `ffmpeg` combined with an available transcription service/tool in your environment) to recover the spoken content. This will tell you the exact network filtering rules.

2. **Develop the Filter in Go:**
   Create a Go project in `/home/user/netfilter/`.
   Write a Go program (`main.go`) that compiles to a binary named `filter`.
   The binary must accept a single command-line argument: the absolute path to a JSON log file representing a network request.
   The JSON format is:
   `{"src_ip": "string", "dst_port": int, "protocol": "string", "payload": "string"}`
   
   Your program must evaluate the JSON against the rules from the voice memo:
   - If the request is benign (clean), the program MUST exit with status code `0`.
   - If the request is malicious (evil), the program MUST exit with status code `1`.

3. **Automation and Process Control:**
   Write a Bash script at `/home/user/setup_ci.sh` that:
   - Builds the Go binary (`/home/user/netfilter/filter`).
   - Generates a valid systemd unit file at `/home/user/netfilter.service` configured to run this binary as a background daemon (even though the automated test will call the binary directly, we need the config file for our CI/CD pipeline). The service should expect the binary to run continuously in production, but your binary for this task only needs to process the single file passed via CLI for verification.

Ensure your Go code handles invalid paths or malformed JSON gracefully (exit 1).