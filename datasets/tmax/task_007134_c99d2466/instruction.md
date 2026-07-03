You are a network security engineer inspecting custom authentication traffic logs. A proprietary authentication service has been crashing, and you need to process its binary traffic captures, correlate them with crash logs, redact sensitive information, and craft a proof-of-concept exploit payload to demonstrate the vulnerability to the vendor.

All integers in this task are little-endian.

**1. Parse and Redact Traffic Logs**
You have a binary traffic capture at `/home/user/traffic_log.bin`. Each record in this file has the following format:
- Timestamp: 4-byte unsigned integer
- Source IP: 4-byte unsigned integer 
- Token Length: 2-byte unsigned integer
- Token: `Token Length` bytes (raw bytes)

Write a C program at `/home/user/analyzer.c` that reads `/home/user/traffic_log.bin` and processes it. 
- A token is considered an "attack" if its length is strictly greater than 50 bytes.
- For all non-attack records (length <= 50), you must redact the Token by replacing every byte of the Token with `0x00` to protect sensitive credentials.
- Attack records must be left unmodified for forensic analysis.
- Write the processed records (with redacted non-attacks and intact attacks) in the exact same binary format to `/home/user/processed_log.bin`.

**2. Correlate with Crash Logs**
The service's system log is at `/home/user/auth_crashes.log`. It contains text entries including crash times.
During your processing in `analyzer.c`, identify the traffic record whose timestamp exactly matches the timestamp of the crash mentioned in `auth_crashes.log`. 
Extract the Token from this specific record and write it as an uppercase hexadecimal string (e.g., `41414141...`) to `/home/user/crash_token.txt`. Do not include any newlines or other characters in this file.

**3. Craft Exploit Payload**
Based on the crash analysis, you determine that the service crashes when it receives a token exactly 128 bytes long that begins with the magic bytes `0xDE 0xAD 0xBE 0xEF`. 
Write a second C program at `/home/user/exploit_gen.c` that, when compiled and executed, generates a file at `/home/user/exploit.bin`.
This file must contain exactly one correctly formatted binary record with:
- Timestamp: `1700000000`
- Source IP: `0x01020304` (representing 4.3.2.1 in little-endian)
- Token Length: `128`
- Token: The first 4 bytes must be `0xDE 0xAD 0xBE 0xEF`, and the remaining 124 bytes must be `0x41` ('A').

Compile and run your C programs to produce the required output files (`/home/user/processed_log.bin`, `/home/user/crash_token.txt`, and `/home/user/exploit.bin`).