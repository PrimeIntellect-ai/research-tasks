You are a security engineer tasked with rotating credentials for a legacy vault system. We have lost the original plaintext password for the admin account, but we have a partial screenshot of the password file and the vault's authentication logs.

Your task involves several steps:

1. **Extract Partial Credentials:** We found an old screenshot of the credential database at `/app/creds_screenshot.png`. Use OCR (e.g., `tesseract`) or other vision tools to extract the readable portion of the admin password. It will look something like `AdminPass: SuperSecret***`, where `***` indicates missing characters.
2. **Identify Target Hash:** Parse the security logs at `/app/auth_logs.txt` to find the most recent failed login attempt for the user `admin`. Extract the password hash associated with this attempt.
3. **Analyze and Optimize the Hash Algorithm:** The custom hashing algorithm used by the vault is provided in C++ source code at `/app/legacy_hash.cpp`. The current implementation is heavily unoptimized. You need to write a C++ password cracking tool at `/home/user/cracker.cpp` that brute-forces the missing characters (which are exactly 4 lowercase alphabetical characters) by appending them to the partial password from the image and hashing it until it matches the target hash from the logs.
4. **Achieve Performance Threshold:** The hash algorithm is computationally intensive. You must optimize the hashing logic in your C++ cracker (e.g., by unrolling loops, vectorization, or algorithmic simplification) so that your brute-force search completes in under 1.5 seconds.
5. **Output the Result:** Once cracked, save the full plaintext password to `/home/user/recovered_password.txt`. Then, use this password to authenticate against the vault binary located at `/app/vault_cli` to rotate the credentials to a new password of your choosing, saving the console output of a successful rotation to `/home/user/rotation_success.log`.

Compile your cracker to `/home/user/cracker` using `g++ -O3 /home/user/cracker.cpp -o /home/user/cracker`. 
Ensure your code is highly optimized, as the automated verification will time its execution.