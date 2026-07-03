You are a forensics analyst tasked with recovering evidence from a compromised host and deploying a quick countermeasure.

During a recent incident, the attacker used an automated tool to execute highly evasive Cross-Site Scripting (XSS) and SQL Injection attacks against our web infrastructure. We have recovered a partial video screen recording from the attacker's machine, located at `/app/evidence.mp4`. The video contains flashing QR codes which represent the raw payload templates the attacker was injecting.

Your task consists of two parts:

1. **Evidence Extraction (Video Analysis):**
   Extract the malicious payload templates from the video `/app/evidence.mp4`. The payloads are embedded as QR codes that flash briefly on the screen. You are encouraged to use `ffmpeg` to extract frames and standard CLI utilities like `zbarimg` to decode the QR codes. 
   Save the decoded raw text payloads to a file named `/home/user/recovered_payloads.txt` (one per line).

2. **Adversarial Filter Creation:**
   Based on your analysis of the recovered injection vulnerabilities, build a robust Bash-based security filter. 
   Create an executable script at `/home/user/detector.sh` that reads a string from `stdin` and classifies it.
   - If the input contains malicious XSS or SQL Injection payloads (matching the patterns/evasion techniques seen in the video or general attack vectors), your script MUST exit with status code `1` (Reject).
   - If the input is completely benign, your script MUST exit with status code `0` (Accept).
   - The script must be completely self-contained and run without network access (simulate process isolation/sandboxing constraints).

An automated verification suite will test your script by piping files from two shipped directories into your script:
- `/app/corpus/evil/`: Contains multiple malicious payloads. Your script must reject 100% of these.
- `/app/corpus/clean/`: Contains typical, benign application inputs (e.g., regular text, names, standard URLs). Your script must accept 100% of these.

Ensure your script handles edge cases, such as trailing spaces, varying capitalization, and URL-encoded variants of the payloads recovered.