You are a forensics analyst responding to a severe incident on a compromised Linux host. An attacker bypassed the web application's Content Security Policy (CSP), injected a malicious script to download a custom payload, and encrypted a set of critical evidence files. 

You must recover the original evidence. 

Here is what we know about the system state:
1. **Attack Logs:** The attacker's initial access vectors and payload downloads were captured in the web server logs located at `/app/nginx/access.log`. You need to analyze these logs to identify the specific CSP bypass/XSS payload the attacker used. Embedded within the attacker's external payload request URL is a numerical seed/key used for the encryption. Extract this integer key.
2. **The Encryptor:** We recovered the attacker's encryption tool at `/app/locker`. It is a stripped binary. Reverse engineer it to understand the encryption mechanism. It takes the integer key as a command-line argument or derives its state from it.
3. **The Encrypted Evidence:** The encrypted files are located in `/app/evidence/` and all end with the `.enc` extension. 

**Your Objectives:**
1. Analyze `/app/nginx/access.log` to extract the integer encryption key. Write ONLY the integer key to `/home/user/recovered_key.txt`.
2. Reverse engineer `/app/locker` to understand the encryption algorithm.
3. Write a decryption program in **C** at `/home/user/decrypt.c` and compile it to `/home/user/decrypt`. Your program should reverse the attacker's algorithm.
4. Process all `.enc` files in `/app/evidence/`. Decrypt them using your compiled C program and the extracted key. 
5. Save the successfully decrypted files into `/home/user/recovered_files/`, preserving the original filenames (remove the `.enc` extension).

**Verification:**
An automated verification script will compute a byte-level accuracy metric comparing the files in `/home/user/recovered_files/` against a hidden backup of the unencrypted evidence. To succeed, your recovered files must perfectly match the originals (Accuracy Metric >= 1.0).