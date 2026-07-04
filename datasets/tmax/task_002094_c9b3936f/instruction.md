You are an incident responder investigating a compromised Linux server. We have gathered some evidence, but part of it is encrypted. We intercepted a voicemail from the suspected insider threat, and we believe it contains the passphrase used to lock the evidence archive.

Here is what you need to do:

1. **Transcribe the Voicemail:**
   Analyze the audio file located at `/app/voicemail.wav`. Recover the spoken English phrase (lowercase, no punctuation, single spacing). 

2. **Unlock the Evidence:**
   Use the transcribed phrase as the password to unzip `/app/evidence.zip` into `/app/evidence/`.

3. **Log Analysis:**
   Inside the extracted files, you will find `logs/auth.log`. Parse this log to identify the IP address of the attacker who successfully authenticated as the `root` user and subsequently executed commands.

4. **ELF Analysis:**
   You will also find an ELF binary named `backdoor_bin` in the extracted files. This binary was used for privilege escalation. Analyze the binary to extract a hardcoded configuration string formatted as `LISTEN_PORT=<port_number>`.

5. **Start the Reporting Service:**
   Write a Python HTTP server that acts as a reporting endpoint. The server must:
   - Listen on `127.0.0.1` using the port number you extracted from the ELF binary in step 4.
   - Implement a `GET /report` endpoint.
   - Return a JSON response with the following exact keys:
     - `"attacker_ip"`: The IP address of the attacker found in step 3.
     - `"transcript"`: The exact extracted passcode from the audio in step 1.
   
   Run your Python server in the background so it remains active. Do not require any authentication to access the `/report` endpoint.

Your final solution should leave the Python HTTP server running on the correct port and serving the required JSON.