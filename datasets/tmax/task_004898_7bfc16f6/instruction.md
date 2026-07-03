You are a network engineer assisting with a security incident. We have intercepted a suspicious encrypted payload from our network traffic, and we need your help to decrypt, analyze, and sanitize it.

Here is what we know and what you need to do:

1. **Key Extraction (OCR)**: We managed to capture a screenshot of the attacker's dashboard during the breach, located at `/app/dashboard.png`. The dashboard displays the AES decryption key. Use OCR (e.g., `tesseract`) to extract this key. Look for a string following "KEY: ".

2. **Payload Decryption**: The intercepted payload is located at `/app/payload.enc`. It is encrypted using AES-256-CBC. The first 16 bytes of the file are the Initialization Vector (IV), and the remainder is the ciphertext. Use the key you extracted to decrypt this file. The decrypted file is an ELF executable. 

3. **Binary Analysis and Sensitive Data Redaction**: The decrypted ELF binary contains multiple hardcoded IP addresses used for command and control. We need to sanitize this binary for external sharing by redacting specific sensitive IP addresses while keeping the ELF format perfectly intact. 
   - Locate all IP addresses belonging to the `10.42.0.0/16` subnet (i.e., starting with `10.42.`).
   - Redact these specific IPs by replacing every character of the matched IP string with the asterisk `*` character (e.g., `10.42.5.12` becomes `**********`).
   - Do NOT modify the length of the file or any other strings/data.

4. **Output**: Save the successfully decrypted and redacted ELF binary to `/home/user/sanitized_payload.elf`. 

Write a Python script at `/home/user/analyze.py` to automate this end-to-end process. You may install any necessary dependencies (like `pytesseract`, `cryptography`, `Pillow`) and run the script to produce the final sanitized binary.