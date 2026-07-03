You are a security engineer tasked with rotating credentials for an internal service and securing the new rotation endpoint against malicious inputs. 

Recently, we discovered that our legacy deployment script was leaking credentials via command-line arguments visible in `/proc`. The old password is no longer known to the team, but a developer left a screenshot of the terminal containing the leaked base64-encoded credential in an image file located at `/app/arch_screenshot.png`. 

Your tasks are as follows:

1. **Extract the Leaked Credential:**
   Use any available tools (e.g., Tesseract OCR is installed) to read the contents of `/app/arch_screenshot.png`. Identify the base64-encoded string representing the old password, decode it, and write the plaintext password to a file exactly at `/home/user/old_password.txt`.

2. **Develop an Input Sanitizer / Vulnerability Detector:**
   The new credential rotation service accepts HTTP requests, but we are concerned about XSS and Injection (SQLi/Command Injection) vulnerabilities in the new logging module. 
   
   You must write a Python script at `/home/user/detector.py` that acts as a standalone payload classifier. The script must:
   - Accept exactly one command-line argument: a file path containing an HTTP payload (simulating an incoming request to the rotation service).
   - Inspect the payload for XSS, SQLi, and Command Injection indicators (e.g., `<script>`, `' OR 1=1`, `; rm -rf`).
   - If the payload is malicious ("evil"), the script must print `EVIL` to stdout and exit with code `1`.
   - If the payload is benign ("clean"), the script must print `CLEAN` to stdout and exit with code `0`.

   To help you develop this, we have provided two directories containing training data:
   - `/home/user/corpus/evil/`: Contains examples of malicious payloads.
   - `/home/user/corpus/clean/`: Contains examples of legitimate credential rotation requests.

Your `detector.py` will be tested against a hidden, much larger test suite of evil and clean payloads. It must successfully classify 100% of the evil payloads as malicious and preserve 100% of the clean payloads as benign.

Ensure your code is efficient and robust against varying payload encodings (e.g., URL encoding).