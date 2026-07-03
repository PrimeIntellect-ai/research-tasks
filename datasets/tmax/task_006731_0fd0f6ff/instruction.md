You are a penetration tester who has extracted a local authentication binary from an embedded device's firmware. The binary file is located at `/home/user/auth_server`.

Through prior reverse engineering, you know the authentication mechanism works as follows:
1. The system accepts a password that is exactly 5 characters long, consisting exclusively of lowercase English letters (`a-z`).
2. The system appends a hardcoded 8-byte salt to the password.
3. It computes the SHA-256 hash of this combined string (password + salt).
4. It compares the computed hash against a hardcoded target hash to grant access.

Both the salt and the target hash are embedded within the binary file (`/home/user/auth_server`):
* The 8-byte salt is located immediately following the 8-byte magic signature `SALT_HDR` (in hex: `53 41 4c 54 5f 48 44 52`).
* The 32-byte target SHA-256 hash is located immediately following the 8-byte magic signature `HASH_HDR` (in hex: `48 41 53 48 5f 48 44 52`).

Your task is to write a Rust program that automates the extraction and cracking process. 
1. Create a new Rust project at `/home/user/cracker`.
2. Write Rust code that reads `/home/user/auth_server`, scans for the magic signatures, and dynamically extracts the 8-byte salt and the 32-byte target hash.
3. Implement a brute-force algorithm within the same Rust program to find the matching 5-character password. You may use standard cryptographic crates (e.g., `sha2`) by adding them to your `Cargo.toml`.
4. Once the password is cracked, write ONLY the 5-character password to `/home/user/solution.txt`.

Note: You have access to the standard internet to download crates via Cargo. Do not attempt to use rainbow tables or external cracking services; the brute-force search space (26^5 = 11,881,376 combinations) is small enough to be computed locally in Rust within seconds.