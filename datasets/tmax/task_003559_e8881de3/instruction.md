You are a DevSecOps engineer responsible for enforcing policy as code on a file upload endpoint. Recently, the endpoint was targeted by a sophisticated attacker who bypassed our legacy Web Application Firewall (WAF) using evasive path traversal and XSS payloads.

Your task consists of two parts:

Part 1: Incident Analysis (Video Forensics)
We have captured a video recording of the attacker's terminal session during the incident, which was encoded as a sequence of QR codes flashing on screen. 
1. The video is located at `/app/incident.mp4`.
2. Extract the frames from this video.
3. Decode the QR codes found in the frames (you may use `zbarimg`).
4. Find the decoded string that starts with `BYPASS_SEED:`. 
5. Save the exact string (e.g., `BYPASS_SEED:example123`) to `/home/user/bypass_seed.txt`.

Part 2: Policy-as-Code WAF (C++)
You must write a C++ program that acts as a robust WAF to analyze file upload metadata and block malicious payloads.
1. Create your C++ source code at `/home/user/waf.cpp`.
2. The program must read from standard input (`stdin`). The input will consist of exactly two lines per execution:
   - Line 1: The `filename` requested by the user.
   - Line 2: The `description` metadata for the file.
3. The program must output exactly `REJECT` to standard output if the input is malicious, or `ACCEPT` if it is clean.
4. An input is considered malicious if it meets ANY of the following criteria:
   - The `filename` contains a path traversal attempt (including basic `../`, as well as URL-encoded variations like `%2e%2e%2f`, `%2e%2e/`, `..%2f`).
   - The `description` contains an XSS payload (e.g., `<script>`, `javascript:`, `onerror=`, `onload=`).
   - Either the `filename` or the `description` contains the exact `BYPASS_SEED` string you recovered in Part 1.
5. If none of the above criteria are met, the input is clean.
6. You must compile your program to an executable located at `/home/user/waf`.

We have provided a training corpus of HTTP requests:
- `/app/corpus/clean/` contains clean requests.
- `/app/corpus/evil/` contains malicious requests.
Your WAF will be evaluated against a hidden, larger adversarial corpus following the same distribution. To pass, your WAF must reject 100% of the evil corpus and accept 100% of the clean corpus.

Ensure your code is efficient and robust against varying upper/lower case encodings for the evasive payloads.