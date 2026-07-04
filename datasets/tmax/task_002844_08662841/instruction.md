You are a security engineer tasked with rotating credentials for a legacy web application. We recently discovered that the legacy authentication service uses a proprietary, unsalted hashing algorithm. We need to crack the existing passwords to notify users of the breach and force rotations, and then secure the system's SSH access.

Here is your workflow:

1. **Reverse Engineer the Hash Algorithm**
   We have recovered the stripped binary used to generate these hashes, located at `/app/legacy_hasher`. 
   If you run `/app/legacy_hasher <password>`, it outputs the 8-character hex hash. 
   Analyze this binary to determine the exact C/C++ algorithm it uses to compute the hash.

2. **Develop an Optimized Cracker in C++**
   The leaked database dump is at `/home/user/dump.txt` (format: `username:hash`).
   A dictionary of potential passwords is at `/home/user/words.txt`.
   Write a highly optimized C++ program at `/home/user/crack.cpp` that recovers the passwords for all users.
   - Your program must read `dump.txt` and `words.txt`.
   - It must output the recovered credentials to `/home/user/cracked.txt` in the format `username:password` (one per line).
   - Because the database and dictionary are large, a naive nested loop will be too slow. You must optimize your approach (e.g., by exploiting the fact that the hashes are unsalted).
   - Compile your code using: `g++ -O3 /home/user/crack.cpp -o /home/user/crack`

3. **SSH Hardening**
   Find the cracked password for the user `admin` in your results.
   Use this password as the passphrase to generate a new `ed25519` SSH keypair at `/home/user/.ssh/id_ed25519`.

**Constraints and Verification:**
- An automated verifier will execute `/home/user/crack` and measure its runtime. It must complete the cracking process in **under 0.5 seconds**. 
- The verifier will also check the validity of `/home/user/cracked.txt` and the newly generated SSH key.
- Do not use external libraries other than the C++ Standard Library.