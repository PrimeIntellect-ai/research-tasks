You are a Site Reliability Engineer (SRE). An automated monitoring system has triggered an alert and left a synthetic voice message containing today's emergency authorization PIN.

Your task is to restore the monitoring webhook by completing the following steps:

1. **Extract the PIN**: Analyze the audio file located at `/app/incident_alert.wav` to extract the 4-digit spoken PIN. You may install and use any tools necessary (like `ffmpeg`, `whisper`, or Python speech recognition libraries) to transcribe the audio. 

2. **Automate Firewall Unlock**: There is an interactive security binary located at `/app/fw_unlock`. It prompts the user with: `Please enter the emergency voice PIN: `. You must write an Expect script at `/home/user/unlock.exp` that spawns this binary, waits for the prompt, sends the 4-digit PIN you extracted, and successfully exits. Run this script to unlock the local firewall (it will create a system flag when successful).

3. **Develop the Monitoring Service**: 
   - Write a C program in `/home/user/monitor_service.c`.
   - The program must start a TCP web server listening on `127.0.0.1:8080`.
   - It must handle incoming HTTP GET requests to the `/status` endpoint.
   - For valid requests, it should respond with a valid `HTTP/1.1 200 OK` header, `Content-Type: application/json`, and the body: `{"status": "UP", "auth": "<PIN>"}`, where `<PIN>` is the 4-digit code from the audio.
   - Compile this program to `/home/user/monitor_service` and run it in the background.

Ensure your C service remains running on port 8080, as it will be actively tested by the automated uptime verifier using the HTTP protocol.