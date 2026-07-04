You are a network engineer analyzing captured authentication traffic. You have intercepted a file containing authentication logs, but you suspect the authentication mechanism is weak and relies on a 4-digit PIN.

Your task is to verify the integrity of the captured log, decode the authentication payloads, and perform a brute-force attack to recover the PINs for each user. You must write a Rust program to perform the cracking.

Here are the details:
1. There is a log file located at `/home/user/capture.json` and its corresponding SHA-256 checksum file at `/home/user/capture.json.sha256`. First, verify the file's integrity. If the file is tampered with, do not proceed (for this task, assume the file provided is intact, but check it anyway).
2. The `capture.json` file contains a JSON array of objects. Each object has two keys: `user` (a string) and `token` (a Base64 encoded string).
3. The `token` is generated using the following custom, weak algorithm:
   - The system creates a string by concatenating the username, a colon (`:`), and a 4-digit PIN (e.g., `admin:1337`).
   - It computes the MD5 hash of this string and outputs it as a lowercase hex string (32 characters).
   - It then Base64 encodes this hex string to produce the final `token`.
4. Create a Rust project in `/home/user/cracker` and write a program that reads `/home/user/capture.json`, decodes the tokens, and brute-forces the 4-digit PIN (from `0000` to `9999`) for each user.
5. Once cracked, output the results to `/home/user/cracked_pins.txt`. Each line should be formatted strictly as `username:PIN`, and the lines must be sorted alphabetically by username.

To accomplish this, you may use standard shell commands and initialize a Rust project using `cargo`. You are allowed to add necessary dependencies (like `md5`, `base64`, `serde`, `serde_json`) to your Rust project.