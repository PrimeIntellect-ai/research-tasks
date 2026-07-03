You are acting as a compliance analyst generating secure audit trails. A recent incident revealed that automated scripts were leaking credentials via command-line arguments visible in process lists, and executing unvalidated inputs leading to potential injection vulnerabilities.

Your objective has two distinct phases:

**Phase 1: Video Artifact Analysis**
We have captured a screen recording of the compromised server's terminal activity during the incident. 
1. The video file is located at `/app/incident_record.mp4`.
2. Extract the frames using `ffmpeg` and analyze them (you may use `tesseract-ocr` which is pre-installed) to identify the exact number of frames where a command containing the exact string `--db-pass=` is visible.
3. Write this integer count to `/home/user/leak_frame_count.txt`.

**Phase 2: Audit Sanitization Filter**
You must write a program to securely filter future audit logs. You may use any language (Python, bash, Node, etc.).
1. The program must be saved as an executable at `/home/user/sanitize_audit`. (Ensure it has executable permissions, e.g., `chmod +x`).
2. The program must read exactly one line of text from `standard input` (representing a logged command).
3. **Redaction:** If the input contains the exact flag `--db-pass=` followed immediately by any non-whitespace characters, replace those characters with `[REDACTED]`. For example, `mysql --db-pass=Secret123 -u root` becomes `mysql --db-pass=[REDACTED] -u root`.
4. **Vulnerability Flagging:** After redaction, check if the resulting string contains either of the exact substrings: `<script>` (XSS indicator) or `; rm -rf` (Command Injection indicator). If either is present, append the exact string ` [FLAG:INJECTION_XSS]` to the end of the output.
5. **Output:** Print the final processed string to `standard output` (with a trailing newline).
6. **Access Control:** Create a locked down directory `/home/user/secure_audit_logs/` with `700` permissions to store future processed logs.

Ensure your `sanitize_audit` program is robust. It will be rigorously tested against thousands of randomized command variations to ensure identical behavior to our strict compliance oracle.