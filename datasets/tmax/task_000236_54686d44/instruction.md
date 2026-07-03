You are an incident response security engineer. A recent breach was captured on a compromised server's screen recording, and the attacker managed to lock our credential vault using our own old master key before dropping a malicious payload. You must recover the key, rotate the credentials, analyze the payload, and deploy an optimized detection script.

**Step 1: Video Analysis & Decryption**
An MP4 screen recording of the incident is located at `/app/incident_screen_record.mp4`. Somewhere in this video, the attacker's terminal displays a QR code that contains the compromised master passphrase.
Extract the passphrase from the video. Use it to decrypt the AES-256-CBC encrypted vault located at `/home/user/vault.enc`. The vault was encrypted using `openssl` with the `-pbkdf2` flag. Decrypt it and extract its contents (a ZIP archive) to `/home/user/vault/`.

**Step 2: Credential Rotation**
Create a new secure random 32-character alphanumeric password. Save this password to `/home/user/new_key.txt`.
You must enforce strict file permissions on `/home/user/new_key.txt` so that only the owner has read access, and no other permissions are granted (0400).
Re-encrypt the contents of `/home/user/vault/` into `/home/user/vault_new.enc` using AES-256-CBC with the new password and `-pbkdf2`.

**Step 3: Malware Analysis & IDS Rule**
Inside the decrypted vault, you will find an ELF binary named `payload.elf`. 
Analyze this binary to extract its unique 12-byte malicious signature. The signature always begins with the hex sequence `DE AD BE EF` and is immediately followed by an 8-byte hardcoded payload ID in the `.rodata` section.
Write an optimized Python script at `/home/user/ids_scanner.py`. This script must act as an Intrusion Detection System log parser. 
It should take two command-line arguments: an input log file path and an output file path.
`python3 /home/user/ids_scanner.py <input_log> <output_log>`

The input log file contains millions of lines of hex-encoded process memory dumps. Your script must find every line containing the 12-byte malicious signature (ignoring spaces in the hex representation) and write the exact original line to the output log.

**Performance Requirement (Metric Threshold):**
Your Python script must be highly optimized. It will be tested against a massive held-out log file (approx. 500,000 lines). 
The verifier will measure the execution time. To pass, your script must process the file and output the correct lines with an execution time of **less than 0.75 seconds**. Ensure you avoid slow regex where simple string matching or byte matching suffices, and use efficient file I/O.