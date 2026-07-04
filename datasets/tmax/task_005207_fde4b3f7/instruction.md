You are a compliance analyst tasked with generating automated audit trails from raw vulnerability and port scanning data. 

Recently, the compliance director left a voicemail detailing the exact data normalization rules required for our new automated vulnerability and privilege escalation auditing pipeline. The voicemail has been saved to the server at `/app/voicemail.wav`.

Your task is to:
1. Process and transcribe the audio file at `/app/voicemail.wav` to recover the exact business logic and normalization rules dictated by the compliance director. (You may install and use any transcription tools or multimedia frameworks necessary).
2. Based on the instructions in the audio, write a standalone executable program located exactly at `/home/user/audit_normalizer`. You may write this in any programming language you prefer, but it must be natively executable or have a proper shebang (e.g., `#!/usr/bin/env python3` or compiled binary) and have executable permissions (`chmod +x`).

The raw scan logs will be piped to your program via Standard Input (`stdin`). Each line of input will be a valid JSON object representing a single scanned endpoint's service and vulnerability data. 

The JSON schema for the input lines is as follows:
- `ip_address`: string (Valid IPv4 address)
- `port`: integer (1 to 65535)
- `service`: string (e.g., "ssh", "http", "mysql")
- `cve_score`: float (0.0 to 10.0)
- `privesc_risk`: boolean (true or false)

Your program must process these JSON lines one by one and write the normalized audit trail to Standard Output (`stdout`), formatted exactly as requested in the audio recording. Do not output any additional text, headers, or debugging information to `stdout`—only the finalized audit trail lines.

Ensure your script handles edge cases gracefully and strictly adheres to the formatting rules specified in the voicemail.