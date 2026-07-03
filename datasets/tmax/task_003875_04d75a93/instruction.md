You are acting as a compliance analyst for a company that recently suffered a data breach. The security team has recovered a proprietary password hashing implementation and a dumped list of compromised accounts, but the original passwords are unknown. Your task is to generate an audit trail of the compromised credentials so the affected users can be notified.

You have been provided with the following files in your home directory (`/home/user/`):
1. `hash_impl.cpp`: The source code containing the custom hashing function (a 32-bit FNV-1a variant) used by the legacy authentication service.
2. `compromised_accounts.txt`: A text file containing the compromised usernames and their corresponding password hashes in the format `username:hash_hex`.

Security intelligence indicates that the legacy system strictly enforced a password policy where **all passwords were exactly 4 lowercase English letters** (e.g., "abcd", "pass").

Your objectives:
1. Write a C++ program (`/home/user/cracker.cpp`) that reverse-engineers or utilizes the logic in `hash_impl.cpp` to brute-force the 4-character lowercase passwords for all hashes found in `compromised_accounts.txt`.
2. Compile and run your program to recover the passwords.
3. Generate a compliance audit report at `/home/user/audit_report.csv`. The file must contain the recovered data in the exact following CSV format: `username,hash_hex,recovered_password`. The rows must be sorted alphabetically by `username`.
4. To ensure the integrity of the audit trail for compliance purposes, compute the SHA-256 checksum of your generated `audit_report.csv` and save the standard `sha256sum` output to `/home/user/audit_report.sha256`.

You must use standard bash utilities and the `g++` compiler. Do not use external libraries outside of the C++ Standard Library. Ensure all output files are placed exactly at the specified paths.