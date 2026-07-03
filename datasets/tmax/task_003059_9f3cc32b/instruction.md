You are acting as an incident responder and security auditor. A recent breach occurred on our internal systems, suspected to involve an open redirect vulnerability in our web application's login flow.

We have gathered the following artifacts for your investigation:
1.  A video capture of the attacker's leaked screen recording found on a paste site, located at `/app/session_capture.mp4`.
2.  An encrypted web server access log, located at `/home/user/encrypted_access.log.enc`.
3.  A backup of the web root directory, located at `/home/user/web_root/`.

Your objectives are to execute the following phases entirely using Bash and standard Linux CLI utilities (ffmpeg is available for video processing):

**Phase 1: Key Extraction**
The video `session_capture.mp4` shows the attacker's terminal. Between seconds 00:03 and 00:05, the attacker accidentally pastes the AES-256-CBC decryption passphrase used to encrypt the web server logs in plain text. Extract frames from this video to recover the passphrase. The passphrase is a 16-character alphanumeric string visible in the center of those specific frames.

**Phase 2: Log Decryption and Analysis**
Use the extracted passphrase to decrypt `/home/user/encrypted_access.log.enc` (using `openssl enc -d -aes-256-cbc -pbkdf2`).
Analyze the decrypted log to find:
- The IP address of the attacker who successfully exploited an open redirect vulnerability (look for suspicious `redirect` parameters leading to external domains followed by an injection attempt).
- The username of the internal user whose session was hijacked immediately after the open redirect event.

**Phase 3: Permission Audit**
The attacker used the hijacked session to upload a web shell because certain files had misconfigured permissions. Scan the `/home/user/web_root/` directory to find all files that are world-writable (permissions `o+w`). 

**Phase 4: Reporting Service**
We need you to stand up an internal reporting endpoint for our automated systems to collect your findings.
Create and run a Bash script that starts an HTTP service listening on `127.0.0.1:8080`.
This service must:
- Accept `POST /report` requests.
- Validate that the request contains an Authorization header with the token `Bearer Incident-Resp-2024`.
- Expect a JSON payload containing your findings.
- If the token is valid, respond with HTTP status `200 OK` and the body `REPORT_RECEIVED`.
- Keep the service running so our verifier can test it.

Store your final findings in a file named `/home/user/findings.json` formatted exactly like this:
```json
{
  "attacker_ip": "X.X.X.X",
  "compromised_user": "username",
  "insecure_files": [
    "/home/user/web_root/path/to/file1",
    "/home/user/web_root/path/to/file2"
  ]
}
```