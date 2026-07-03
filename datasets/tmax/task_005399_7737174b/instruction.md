You are a compliance analyst generating audit trails for a recent security breach. The breach occurred via a file upload handler that was susceptible to path traversal attacks, allowing an attacker to overwrite sensitive SSH keys.

Your task consists of two parts: Investigation and Remediation.

### Part 1: Investigation (Video Analysis & SSH Cracking)
A security camera in the server room captured a brief glimpse of a physical sticky note containing a partial 4-digit PIN used to encrypt the backup SSH key.
1. Analyze the security footage located at `/app/server_room.mp4`. The video is 5 seconds long. Around the 3-second mark, a sticky note is visible showing a partial PIN (e.g., `12??`, where `?` represents illegible digits).
2. The encrypted SSH private key is located at `/app/backup_id_rsa`.
3. Use your password cracking/brute-force skills to find the missing two digits. The passphrase for the SSH key is exactly the 4-digit PIN.
4. Once you have successfully brute-forced the PIN and verified it unlocks `/app/backup_id_rsa`, write the 4-digit PIN to `/home/user/cracked_pin.txt`.

### Part 2: Remediation (Secure Coding & Vulnerability Analysis)
To prevent future path traversal attacks in the upload handler, you must write a strict filename sanitization filter in C.
1. Create a C program at `/home/user/path_filter.c` and compile it to `/home/user/path_filter`.
2. The compiled binary must accept exactly one argument: the filename string to check.
   Example: `./path_filter "../../../etc/passwd"`
3. The program must evaluate the filename and exit with specific status codes:
   - Exit Code `0`: The filename is SAFE (clean).
   - Exit Code `1`: The filename is MALICIOUS (contains path traversal vectors).
4. Your filter must detect common path traversal patterns, including but not limited to:
   - Standard directory traversal (`../` or `..\`)
   - URL-encoded dot-dot-slash variations (e.g., `%2e%2e%2f`, `%2e%2e/`, etc.)
   - Null byte injections (`%00` or `\0`)
5. Your filter must safely allow normal filenames, including those with standard single dots (e.g., `report.pdf`, `archive.tar.gz`, `valid_dir/file.txt`).

An automated test suite will evaluate your `/home/user/path_filter` binary against an adversarial corpus of "evil" filenames and a corpus of "clean" filenames. You must correctly classify 100% of both corpora.