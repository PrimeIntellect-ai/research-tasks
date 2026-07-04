You are an incident responder investigating a compromised file upload handler that suffered a path traversal attack. 

We have recovered a fragmented video recording of the attacker's traffic generation tool, located at `/app/incident.mp4`. We also know the attacker used a custom evasion prefix alongside standard path traversal sequences to bypass our legacy filters.

Your task is divided into two parts:

**Part 1: Video Analysis for Evasion Artifacts**
The video `/app/incident.mp4` contains exactly 64 frames. Each frame represents a single bit of an 8-character ASCII string (the attacker's custom evasion prefix). 
- If the top-left 50x50 pixel region of the frame is pure white (`#FFFFFF`), the bit is `1`.
- If the top-left 50x50 pixel region is pure black (`#000000`), the bit is `0`.
Extract these frames, decode the 64 bits into an 8-character ASCII string, and use it in Part 2.

**Part 2: Build the Intrusion Detection Classifier**
Write a robust Python script at `/home/user/detector.py` that acts as a sanitizer/classifier for incoming filenames.
- The script must take a single command-line argument: the path to a text file containing the filename payload. Example: `python3 /home/user/detector.py payload.txt`
- The script must evaluate the contents of the payload file and print exactly `EVIL` to standard output if the payload is malicious, or `CLEAN` if it is safe.
- A payload is `EVIL` if it contains:
  1. Standard directory traversal attempts (e.g., `../`, `..%2f`, `%2e%2e%2f`, etc., case-insensitive).
  2. Absolute path injections (starting with `/`).
  3. Null byte injections (`%00` or `\x00`).
  4. The exact 8-character custom evasion prefix you recovered from the video in Part 1.
- A payload is `CLEAN` if it is a standard relative filename (e.g., `image.png`, `docs/report.pdf`, `archive_2023.tar.gz`) without any of the above threats.

Your classifier will be programmatically tested against a hidden adversarial corpus. To succeed, your script must correctly classify 100% of the evil payloads and 100% of the clean payloads.