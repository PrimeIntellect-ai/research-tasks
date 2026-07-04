You are a penetration tester investigating a newly discovered Command and Control (C2) infrastructure that targets web applications. We have intercepted an encrypted archive containing the C2's web payload traffic, along with an audio recording of a voicenote left by one of the operators.

Your objective is to extract the traffic, analyze the vulnerabilities being exploited, and build a Python-based Web Application Firewall (WAF) to detect these specific attacks.

Step 1: Extract the Corpora
You have been provided with an audio file at `/app/voicenote.wav`. This file contains an operator reading out the passphrase used to encrypt the payload archive.
1. Transcribe the audio file to recover the passphrase.
2. Use the recovered passphrase to decrypt and extract the archive located at `/app/traffic_dump.zip`.
3. The extracted archive will create two directories: `/home/user/traffic/evil/` (containing files with malicious C2 web payloads) and `/home/user/traffic/clean/` (containing benign web traffic payloads).

Step 2: Build the Intrusion Detection System
The malicious payloads in the `evil` directory employ a custom evasion technique combining SQL injection patterns with specific hexadecimal encoding tricks and padded whitespace that bypasses standard filters. 
You must analyze the files in both the `evil` and `clean` directories to understand the pattern the attackers are using, while ensuring normal traffic isn't flagged.

Step 3: Implementation
Write a Python script at `/home/user/waf.py` that implements a detection function.
Your script MUST contain the following function signature:
`def scan_payload(filepath: str) -> bool:`

- The function should take the absolute path to a text file containing a web payload.
- It must return `True` if the file contains a malicious payload (evil).
- It must return `False` if the file contains benign traffic (clean).

Your solution will be tested against a hidden, held-out dataset of evil and clean payloads that follow the exact same grammatical and encoding rules as the provided corpora. You must ensure your regex pattern matching or string analysis is robust and does not hardcode specific file names.