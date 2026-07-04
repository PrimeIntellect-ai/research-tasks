You are a Linux Systems Engineer tasked with hardening the SSH configurations for our servers. 

Your senior administrator has left a voicemail recording for you at `/app/voicemail.wav`. This recording contains the exact specification for a new custom SSH access filtering script.

Your tasks are:
1. Listen to or transcribe the `/app/voicemail.wav` file to understand the new filtering rules. You may use any available tools (like `ffmpeg`, `whisper`, or standard Python libraries if applicable, though you may need to install standard transcription CLI tools).
2. Write a Python script at `/home/user/filter.py` that implements these exact rules. 
    - The script must read a single line from `stdin`.
    - The input line will contain a username and an IP address, separated by a single space (e.g., `adminuser 192.168.1.50`).
    - The script must evaluate the input against the rules in the voicemail and print strictly `ALLOW` or `DENY` to `stdout`.
    - Do not print any other text, warnings, or prompts.
3. Configure your local SSH client config file (`/home/user/.ssh/config`) to include a `Host` block for `local_tunnel` pointing to `127.0.0.1` on port `2222`. (We will use this later for process supervision and tunneling).

Ensure your Python script is robust against malformed inputs (if the input doesn't match the `<username> <IP>` format, it should default to `DENY`). Your script will be rigorously tested against thousands of randomized inputs to ensure it perfectly matches the requested logic.