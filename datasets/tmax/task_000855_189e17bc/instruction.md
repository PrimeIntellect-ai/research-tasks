You are acting as a security engineer supporting a red-team operation. We are testing a newly deployed egress filter designed to prevent sensitive data exfiltration. An open redirect vulnerability in our web server's login flow was recently discovered, and attackers have been trying to use it to exfiltrate SSH private keys and redirect users to a malicious domain.

Your task is to build a sensitive data redaction tool, perform file integrity verification, and securely configure SSH.

**Step 1: Secure SSH Configuration**
Generate a new ED25519 SSH keypair at `/home/user/.ssh/id_ed25519` (no passphrase). 
Create an SSH config file at `/home/user/.ssh/config` that applies to all hosts (`Host *`) and explicitly disables password authentication (`PasswordAuthentication no`). Ensure the directory and file permissions are secure.

**Step 2: Identify the Malicious Domain**
We captured a screenshot from the threat actor's control panel. It is located at `/app/exfil_target.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to read the text in this image. Somewhere in the text, it identifies the "Target Domain". You will need this exact domain name for Step 3.

**Step 3: Build the Redaction Filter**
Create an executable script at `/home/user/redactor.py` (you may use Python, Ruby, or a shell script with awk/sed, but it must be executable and handle arguments). 
The script must take a single file path as its first command-line argument, read the file, and print the sanitized text to standard output (`stdout`). 
It must apply the following redaction rules:
1. **Open Redirect Payload:** Find any continuous non-whitespace sequence (word) that begins with `http://` or `https://` AND contains the malicious domain you extracted in Step 2. Replace that entire word with the literal string `[REDACTED_URL]`.
2. **Leaked SSH Keys:** Detect any SSH private key block. This includes the header line (e.g., `-----BEGIN RSA PRIVATE KEY-----` or `-----BEGIN OPENSSH PRIVATE KEY-----`), the base64 payload, and the footer line (e.g., `-----END RSA PRIVATE KEY-----`). Replace the *entire* key block with the literal string `[REDACTED_KEY]`.

**Step 4: File Integrity Verification**
We have provided a corpus of text files to test your filter under `/app/corpus/clean/` and `/app/corpus/evil/`.
Before testing, calculate the SHA-256 hashes of all the files inside the `/app/corpus/clean/` directory. Save the output to `/home/user/clean_hashes.txt` in the standard `sha256sum` format.

**Verification:**
An automated suite will test your script by passing files from the clean and evil corpora into your script and evaluating standard output. Your script must leave 100% of the clean corpus completely unmodified, while perfectly redacting the sensitive strings in 100% of the evil corpus files.