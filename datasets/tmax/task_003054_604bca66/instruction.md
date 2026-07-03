You are acting as a compliance analyst for a security firm. A system administrator's terminal session was recorded during an incident response, and you need to generate an audit trail of the commands executed. However, the administrator inadvertently exposed sensitive authentication data and credentials during the session.

Your task is to build a robust bash-based redaction tool, and then use it to process the video recording of the terminal session.

**Step 1: Create the Redaction Script**
Write a bash script at `/home/user/redact.sh` that takes a single file path as an argument and prints the sanitized contents to standard output.
You must implement redaction for the following sensitive data patterns:
1. **AWS Access Keys**: Any string starting with `AKIA` followed by exactly 16 uppercase alphanumeric characters (e.g., `AKIAIOSFODNN7EXAMPLE`). Replace the exact 20-character match with `[REDACTED_AWS]`.
2. **URL Credentials**: Any password embedded in an HTTP/HTTPS URL (e.g., `http://username:secretpass@example.com`). Replace the password portion with `[REDACTED_CREDS]`. The resulting URL should look like `http://username:[REDACTED_CREDS]@example.com`.

Your script must preserve all other text exactly as it is. We will test your script against a hidden suite of logs.

**Step 2: Process the Video Audit Trail**
The video file of the terminal session is located at `/app/admin_session.mp4`.
1. Extract the frames from the video. The video is exactly 3 seconds long at 1 frame per second (yielding 3 frames).
2. Extract the text from each frame. You may install and use `tesseract-ocr` for this purpose.
3. Concatenate the text from the 3 frames in chronological order into a single text stream.
4. Process this text using your `/home/user/redact.sh` script.
5. Save the final, redacted text to `/home/user/audit_trail.txt`.

Ensure your redaction script handles edge cases robustly, as the automated tests will evaluate `/home/user/redact.sh` against an adversarial corpus of "evil" files (containing various tricky credential injections) and "clean" files (which must not be altered).