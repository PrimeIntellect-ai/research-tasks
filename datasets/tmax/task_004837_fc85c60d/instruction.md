As a DevSecOps engineer enforcing policy as code, you are auditing a legacy privilege escalation mechanism. 

We have discovered an old, stripped binary at `/app/legacy_auditor` that is currently used to decrypt access tokens and determine if a user has privilege escalation rights. Because it is a compiled black box, we cannot easily audit its logic or integrate it into our modern policy-as-code pipeline, and it runs too slowly to process our daily logs of millions of access attempts.

Your task is to:
1. Reverse engineer the decryption algorithm used by the stripped binary `/app/legacy_auditor`. The binary takes two arguments: a hex-encoded ciphertext token and a string key. It outputs the decrypted plaintext policy. 
   Example usage: `/app/legacy_auditor <hex_ciphertext> <key>`
2. Write a highly efficient C++ program at `/home/user/fast_auditor.cpp` that replicates this decryption logic. 
3. Your C++ program must accept an input file path and an output file path as command-line arguments:
   `./fast_auditor <input_file> <output_file>`
4. The input file will contain one entry per line in the format: `<hex_ciphertext> <key>`.
5. For each line, your program must decrypt the token. If the resulting plaintext contains the exact substring `escalation=granted`, it must write the original `<hex_ciphertext>` to the output file (one per line).
6. Compile your program to `/home/user/fast_auditor` (e.g., `g++ -O3 /home/user/fast_auditor.cpp -o /home/user/fast_auditor`).

The automated verifier will evaluate your compiled C++ binary against a hidden dataset of 500,000 tokens to ensure both algorithmic equivalence and execution performance.