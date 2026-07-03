You are a forensics analyst responding to a compromised Linux host. The attacker managed to execute commands that leaked sensitive credentials into the process list (visible via `/proc`), and they tampered with the local firewall to block outgoing telemetry. 

You have been provided with two pieces of evidence:
1. `/app/attack_recording.mp4`: A screen recording of the attacker's terminal session. Somewhere in this video, the attacker adds an `iptables` rule to drop outbound TCP traffic to a specific port.
2. `/app/trusted_roots.pem`: A bundle of trusted certificates used by the system's telemetry service.

Your objective is to write a precise log sanitization script that will process the recovered process logs, redact sensitive HTTP headers and credentials, filter out blocked traffic, and tag trusted telemetry.

**Task Requirements:**

1. **Analyze the Video**: Inspect `/app/attack_recording.mp4` (you can use `ffmpeg` to extract frames). Find the specific destination port (`--dport`) that the attacker blocked using `iptables`.
2. **Analyze the Certificate**: Extract the `Common Name` (CN) of the **first** certificate in the `/app/trusted_roots.pem` bundle.
3. **Create the Sanitizer**: Write a Python 3 script at `/home/user/redactor.py` that reads log lines from `standard input` (stdin), processes each line exactly according to the rules below, and writes the result to `standard output` (stdout).

**Sanitization Rules for `/home/user/redactor.py`:**
Apply these rules to every line read from stdin, in order:
* **Rule 1 (Firewall Filter):** If the line contains the exact port number blocked by the attacker (as a string anywhere in the line), **drop the line entirely** (do not output it at all, move to the next line).
* **Rule 2 (Redact Passwords):** Replace any occurrence of `--password <word>` with `--password REDACTED` (where `<word>` is any sequence of non-whitespace characters).
* **Rule 3 (Redact Cookies):** Replace any occurrence of `Cookie: <word>` with `Cookie: REDACTED`.
* **Rule 4 (Redact Auth Tokens):** Replace any occurrence of `Authorization: Bearer <word>` with `Authorization: Bearer REDACTED`.
* **Rule 5 (Tag Trusted Telemetry):** If the line contains the exact Common Name (CN) extracted from the first certificate in the PEM bundle, append the exact string ` [TRUSTED]` to the end of the line (just before the newline character).

**Execution Contract:**
* Your script must be executable as `python3 /home/user/redactor.py`.
* It must read from `sys.stdin` and write to `sys.stdout`.
* An automated fuzzing verifier will pipe thousands of randomized log lines into your script and compare your script's output bit-for-bit against a secret reference implementation. Ensure your regex / string replacements are precise and only target exactly what is specified. Do not add extra spaces or change unmodified text.