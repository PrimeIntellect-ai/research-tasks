You are a security researcher analyzing a suspicious data ingestion binary that has been crashing intermittently. You have been provided with a crash trace, a video recording of the system dashboard during a known attack, and a set of test logs.

The ingestion system processes telemetry logs. The log format is space-separated:
`TIMESTAMP PRESSURE_VALUE STATUS`
Example: `1715000001 104.1234 OK`

**The Vulnerabilities:**
1. **Precision Crash:** Stack trace analysis reveals the binary uses an unsafe fixed-size buffer to parse the `PRESSURE_VALUE` float. If the float has more than 4 decimal places (e.g., `104.12345`), or uses scientific notation (e.g., `1.04e2`), it causes a buffer overflow and a core dump.
2. **Malicious Injection Window:** An attacker manipulated the pressure sensors during a specific time window. A screen recording of the system dashboard is available at `/app/dashboard.mp4`. The video displays a Unix timestamp on screen that increments every second. You must extract frames from this video to determine the exact start and end Unix timestamps (inclusive) during which the word "OVERLOAD" appears on the screen in red text.

**Your Objective:**
Write a Bash script at `/home/user/sanitize.sh` that acts as a secure filter.
Your script must accept a single log file path as an argument (`$1`) and output the sanitized log data to standard output (`stdout`).

**Sanitization Rules:**
1. If a line's `TIMESTAMP` falls within the "OVERLOAD" window observed in the video, **drop the line completely**.
2. If a line's `PRESSURE_VALUE` contains scientific notation (contains `e` or `E`), **drop the line completely**.
3. If a line's `PRESSURE_VALUE` has more than 4 decimal places, **truncate the fractional part to exactly 4 decimal places** (do not round, just truncate, e.g., `12.56789` becomes `12.5678`).
4. All other lines must be passed through **exactly unchanged** (preserving original spacing and format).

**Verification:**
Your script will be tested against an adversarial corpus and a clean corpus of log files. 
- The clean logs must be output exactly identical to their input.
- The evil logs (which contain crash-inducing precision or attack-window timestamps) must be sanitized precisely according to the rules above.