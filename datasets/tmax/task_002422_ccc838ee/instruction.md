You are acting as a security engineer analyzing a recent breach. The attacker exploited a file upload handler susceptible to path traversal by uploading polyglot files—files that are valid images but also contain malicious ELF headers or embedded injection/XSS payloads. 

First, analyze the initial evidence file left by the attacker at `/app/evidence.png`. The attacker embedded a hidden string (a "seed" or password) in this image using basic text embedding visible via OCR or string extraction. You will need to extract this string.

Second, the attacker generated a massive set of evasion payloads. We have captured a dataset of these files. Your objective is to build a Python-based classifier (filter) to prevent this in the future.
We have provided two directories:
- `/app/corpus/evil/`: Contains 50 malicious polyglot images that contain path traversal patterns, XSS payloads, or disguised ELF execution triggers.
- `/app/corpus/clean/`: Contains 50 benign, normal images.

Write a Python script at `/home/user/filter.py`. The script must take a single file path as a command-line argument:
`python3 /home/user/filter.py <path_to_file>`

Requirements:
1. The script must parse the binary format of the file to detect anomalies, ELF signatures embedded within image chunks, or path traversal/XSS strings.
2. If the file is malicious (matches the evil corpus behavior), the script must exit with status code `1` (Reject).
3. If the file is benign (matches the clean corpus behavior), the script must exit with status code `0` (Accept).
4. Do not just hardcode the filenames; your script must dynamically analyze the content.
5. Save your extracted seed from the evidence image to `/home/user/extracted_seed.txt`.