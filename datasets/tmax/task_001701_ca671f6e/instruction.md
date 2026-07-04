You are a platform engineer maintaining the security pipeline for our CI/CD build system. Recently, we received an automated incident report via a voice memo from the security team, but the automated pipeline failed to transcribe it and apply the necessary security rules.

Your task is to implement a high-performance log filtering step in our pipeline using Bash. 

1. **Audio Extraction**: Listen to or transcribe the audio file located at `/app/auth_payload.wav`. It contains a spoken incident report that identifies a specific malicious IP address that must be blocked completely.
2. **Log Filtering and Rate Limiting**: You have a large access log file at `/app/access.log`. The file format is space-separated: `[UnixTimestamp] [IP_Address] [HTTP_Method] [Path]`.
   Write a highly optimized Bash script at `/home/user/filter_logs.sh` that takes `/app/access.log` as its first argument and writes the filtered logs to `/home/user/filtered.log`.
   
   Your script must enforce the following rules:
   - **Rule A (Blacklist)**: Completely drop any log lines originating from the malicious IP address identified in the audio file.
   - **Rule B (Rate Limiting)**: For all other IPs, enforce a strict rate limit of **maximum 5 requests per calendar minute** (i.e., grouped by the minute portion of the Unix timestamp, calculated as `Timestamp / 60`). Any requests from an IP exceeding this count within the same minute window must be dropped.

3. **Performance Requirement**: The access log contains hundreds of thousands of lines. Pure Bash loops will be too slow. Your script must process the file extremely quickly. You are encouraged to use fast Unix utilities (like `awk`, `sed`) or have your bash script compile and execute a minimal, highly optimized C or assembly helper program to perform the rate limiting.

Ensure your final script `/home/user/filter_logs.sh` is executable and generates exactly the allowed requests in `/home/user/filtered.log` in the original format.