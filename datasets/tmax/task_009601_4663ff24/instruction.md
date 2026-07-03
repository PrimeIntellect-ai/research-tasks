You are acting as a penetration tester analyzing a custom authentication mechanism found on a compromised Linux system. 

In the directory `/home/user/vuln_scan/`, you will find two files:
1. `auth_checker` - A stripped, compiled C++ ELF executable that verifies 4-digit PINs. 
2. `hashes.txt` - A text file containing a list of cryptographic hashes corresponding to different user PINs extracted from a database.

Your analysis indicates that `auth_checker` uses a hardcoded salt and the SHA256 hashing algorithm. The hashing format used is `SHA256(salt + PIN)`, where `PIN` is exactly 4 digits (e.g., "0000" to "9999").

Your tasks:
1. Use command-line analysis/reverse-engineering tools to inspect the `auth_checker` binary and discover the hardcoded salt string.
2. Write a C++ program at `/home/user/vuln_scan/cracker.cpp` to brute-force the 4-digit PIN for each hash in `hashes.txt`. You may use the OpenSSL library (`<openssl/sha.h>`) for hashing. Compile it using `g++ -O3 cracker.cpp -lcrypto -o cracker`.
3. Run your cracker and output the results to `/home/user/vuln_scan/cracked.txt`.

The format of `/home/user/vuln_scan/cracked.txt` must be exactly:
```
<hash1>:<4-digit-PIN>
<hash2>:<4-digit-PIN>
...
```
Order the output in the same order as the hashes appear in `hashes.txt`.

Ensure your C++ program handles the brute-force search efficiently and correctly concatenates the discovered salt and PIN before hashing.