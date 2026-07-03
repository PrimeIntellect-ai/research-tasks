We have intercepted a screen recording (`/app/attack_session.mp4`) of a red-team operator testing a custom evasion tool. This tool mutates XSS and SQL injection payloads to bypass our WAF. 

Your objective is to:
1. Extract frames from the video to reverse-engineer the evasion payload's encoding mechanism. The operator's terminal shows the exact command and parameters used to obfuscate a known payload.
2. Based on your cryptanalysis and reverse-engineering of the technique shown in the video, write a robust detector script at `/home/user/detector.py`.

The script `/home/user/detector.py` must:
- Be an executable Python 3 script.
- Accept a single command-line argument: the path to a directory containing text files.
- Read each file in the directory.
- Determine if the file's contents represent an obfuscated malicious payload using the attacker's technique.
- Print the filename (just the basename, e.g., `payload_01.txt`) of every malicious file to `stdout`, one per line. Do not print the names of benign files.

We will evaluate your detector against an adversarial corpus. Your script must successfully flag 100% of the malicious payloads and ignore 100% of the benign inputs.