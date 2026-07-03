You are a forensics analyst recovering evidence from a compromised host. You have discovered a suspicious C source file left by the attacker at `/home/user/backdoor.c` and an encrypted data blob at `/home/user/evidence.enc`.

Your objectives are:
1. Analyze the authentication flow and cryptographic logic in `/home/user/backdoor.c`.
2. Compile the C code into an executable.
3. Craft a valid payload (password) that satisfies the authentication constraints. The constraints require specific character sums and positions to trigger the exploit/decryption function.
4. Execute the compiled backdoor with your crafted password to decrypt the evidence. The backdoor will output the decrypted file to `/home/user/recovered.dat` upon successful authentication.
5. Compute the SHA256 checksum of `/home/user/recovered.dat` to verify its integrity.
6. Save ONLY the SHA256 checksum (the 64-character hex string) to a file named `/home/user/evidence_hash.txt`.

Ensure your crafted payload exactly meets the constraints in the C code. You may write additional scripts or C code to generate the payload if necessary.