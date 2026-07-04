You are acting as a security engineer tasked with rotating compromised credentials and building a detection script for an open redirect vulnerability that was actively exploited in our web server's login flow.

Your tasks are:
1. **Recover the Old Credential**: We lost the original text file containing the old master password, but a screenshot of the console when it was generated is available at `/app/screenshot.png`. Extract the old master password from this image.
2. **Reverse Engineer the Hash Algorithm**: The authentication service's source code was lost, but a compiled bytecode file remains at `/app/auth_service.pyc`. Decompile or inspect this file to understand how the system generates password hashes. It uses the old password as part of the hashing process.
3. **Rotate the Credential**: Using the algorithm discovered in step 2, generate the new password hash for the new password `RotateMeNow2024!` using the extracted old password where required by the algorithm. Save ONLY the resulting hex string to `/home/user/new_hash.txt`.
4. **Detect Open Redirect Exploitation**: Write a Python script at `/home/user/detect_redirects.py` to parse standard Nginx access logs and identify IP addresses that attempted to exploit the open redirect vulnerability on the `/login` endpoint (e.g., passing absolute external URLs in parameters like `next`, `return_to`, or `redirect`).
   - The script must take the log file path as its first and only command-line argument.
   - It must print a valid JSON array of strings (the unique malicious IP addresses) to `stdout`.
   - Ensure your regex/parsing logic correctly differentiates between valid internal redirects (e.g., `?next=/dashboard`) and malicious external redirects (e.g., `?next=http://evil.com` or `?next=//evil.com`).

**Evaluation**:
Your `detect_redirects.py` script will be evaluated against a hidden, held-out Nginx access log file containing various obfuscated open redirect attempts and benign traffic. To pass, your script's output must achieve an F1 score of $\ge 0.90$ compared to the ground truth of malicious IPs. The content of `/home/user/new_hash.txt` will also be checked for exact correctness.