You are a network security engineer investigating a recent intrusion. 
During the incident, you intercepted a VoIP communication stored at `/app/intercept.wav` and a network traffic dump exported as `/app/traffic.log`.

Your objectives:
1. **Transcribe the Audio**: Analyze `/app/intercept.wav` to extract the spoken SSH key suffix. (You may use available tools like `whisper` or `ffmpeg` + standard transcription libraries available in standard repositories).
2. **Payload Decoding**: The file `/app/traffic.log` contains multiple lines, each with a Base64-encoded SSH public key payload in the format `PAYLOAD:<base64_string>`.
3. **C++ Implementation**: A skeleton C++ program exists at `/home/user/process_keys.cpp`. You must complete this program so that it:
   - Reads `/app/traffic.log`.
   - Decodes the Base64 payloads.
   - Identifies the specific SSH key whose decoded string ends with the suffix mentioned in the audio intercept (ignoring standard base64 padding if spoken as "equals").
   - Redacts any sensitive internal IP addresses (e.g., `10.x.x.x`) found within the comments of the decoded SSH keys, replacing them with `[REDACTED]`.
4. **SSH Hardening**: Have your C++ program (or a subsequent bash command) write the correctly identified and redacted SSH public key to `/home/user/authorized_keys`. Ensure the file has the strict, correct access permissions required by SSH daemon standards.

Ensure your C++ program compiles with `g++ -O2 -std=c++17 /home/user/process_keys.cpp -o /home/user/process_keys`.

Your final output must be the perfectly constructed `/home/user/authorized_keys` file. Automated verification will measure the string similarity of your output against the exact required key.