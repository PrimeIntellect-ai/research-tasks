You are a security engineer tasked with rotating credentials and deploying a new input validation filter for the credential management service.

Step 1: The new master password for our secure storage has been provided as an image backup at `/app/master_pass.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to extract the text from this image.

Step 2: We have an encrypted archive of historical credential rotation requests at `/app/payloads.tar.gz.enc`. Decrypt this archive using `openssl` with the `aes-256-cbc` cipher and `-pbkdf2`. Use the master password you extracted in Step 1 as the passphrase (e.g., `-pass pass:<extracted_password>`). Extract the resulting archive into `/home/user/payloads/`.

Step 3: Inside the extracted archive, you will find two directories: `clean/` (containing valid, benign credential update strings) and `evil/` (containing attempts at SQL Injection, Cross-Site Scripting (XSS), and Command Injection). 

Step 4: Write a Go program at `/home/user/validator.go` and compile it to `/home/user/validator`. This program must:
- Accept exactly one command-line argument: the absolute path to a text file.
- Read the contents of the file.
- Analyze the contents for signs of Injection or XSS vulnerabilities (e.g., checking for shell metacharacters, SQL operators like `' OR`, or HTML/script tags).
- Terminate with exit code `0` if the contents are perfectly clean and safe.
- Terminate with exit code `1` if the contents contain any malicious payload.

Your final deliverable is the compiled binary `/home/user/validator` which effectively filters out the malicious files while allowing the clean ones. Ensure your Go code correctly handles basic file I/O and exits with the required status codes.