You are a security engineer tasked with rotating a credential for a legacy system. The original password has been lost, and the system uses a proprietary, undocumented hashing algorithm. 

You have been provided with the legacy authentication binary located at `/home/user/legacy_auth`. This binary takes a single string argument and prints its custom hash in hexadecimal format. 

We know the following about the lost credential:
- It consists of exactly 5 lowercase English letters (e.g., `abcde`).
- Its generated hash is `0x2e99f19`.

Your objectives are:
1. Reverse engineer the `/home/user/legacy_auth` binary to understand the custom cryptographic hashing algorithm.
2. Write a highly efficient C program at `/home/user/cracker.c` that implements this algorithm and brute-forces the 5-lowercase-letter password that results in the hash `0x2e99f19`.
3. Compile and run your cracker. Save the recovered plaintext password to `/home/user/recovered_password.txt` (just the 5-letter string, no newline required).
4. As part of the credential rotation process, compute the hash for the new password `securekey` using the same custom algorithm.
5. Save this new hash (formatted exactly as the binary outputs it, e.g., `0x...`) to `/home/user/new_credential.txt`.

Constraints & Details:
- Do not attempt to brute-force by invoking the `legacy_auth` binary repeatedly using a shell script, as the overhead will be too slow. You must implement the algorithm in C.
- The standard C compiler (`gcc`) and reverse engineering tools like `objdump`, `gdb`, and `ltrace` are available on the system.