You are a compliance analyst tasked with generating a secure, verifiable audit trail from a set of raw, encoded system event logs. 

You have been provided with a file at `/home/user/raw_audits.txt`. This file contains several lines of raw audit payloads. Each line is a Base64-encoded string representing a distinct system event.

Your objective is to write a C program at `/home/user/audit_processor.c` that performs the following operations:
1. Opens and reads `/home/user/raw_audits.txt`.
2. Decodes each Base64-encoded payload.
3. Computes the SHA-256 cryptographic hash of the *decoded* payload.
4. Writes the results to a new audit log file located at `/home/user/secure_audit.log`.

The output in `/home/user/secure_audit.log` must contain exactly one line per event, formatted precisely as follows:
`<SHA256_HEX>:<DECODED_TEXT>`
(Note: `<SHA256_HEX>` must be lowercase).

After your C program generates `/home/user/secure_audit.log`, you must ensure that this generated log file is protected from unauthorized modification or access. Use shell commands to set the file permissions of `/home/user/secure_audit.log` so that only the owner has read permissions, and no other permissions are granted to anyone (i.e., `0400` or `-r--------`).

Requirements:
- You must write the solution primarily in C (`/home/user/audit_processor.c`).
- You may use OpenSSL (`libssl-dev`, linking with `-lcrypto`) to assist with the Base64 decoding and SHA-256 hashing. You are free to install any necessary packages using `sudo apt-get`.
- Do not append any trailing spaces or newlines to the decoded text when hashing; hash exactly the decoded bytes.
- Do not include newline characters from the raw text file in your Base64 decoding process.