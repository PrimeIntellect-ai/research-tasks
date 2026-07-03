You are a security engineer tasked with completing a stalled credential rotation process. The engineer previously handling this left the company suddenly, leaving behind only a few artifacts in `/home/user/`.

You need to recover the old legacy password to decrypt the new configuration, and then perform an incident response scan on the server logs to identify any unauthorized access attempts using that compromised legacy password.

Here are the artifacts you have in `/home/user/`:
1. `/home/user/legacy_hash.cpp` - A C++ file containing the proprietary string hashing algorithm used for the old passwords.
2. `/home/user/old_hash.txt` - A text file containing the unsigned 32-bit integer hash of the old legacy password. You know the old password consisted of exactly 5 lowercase English letters (a-z).
3. `/home/user/new_config.enc` - The new configuration file, encrypted using `openssl` with the AES-256-CBC cipher and PBKDF2. The encryption password is the 5-letter old legacy password.
4. `/home/user/auth_access.log` - An authentication log from the legacy application.

Perform the following steps:
1. **Password Cracking:** Analyze the hashing algorithm in `legacy_hash.cpp`. Write a C++ program to brute-force the 5-lowercase-letter password that produces the target hash found in `old_hash.txt`. 
2. **Decryption:** Use the recovered 5-letter password to decrypt `/home/user/new_config.enc` using the OpenSSL CLI. Inside the decrypted file, you will find a key-value pair `NEW_CREDENTIAL=<the_new_password>`.
3. **Intrusion Detection:** Scan the `/home/user/auth_access.log` file. Find all unique IP addresses that attempted to log in using the exact 5-letter old legacy password AND resulted in a `STATUS:REJECTED`.
4. **Reporting:** Create a JSON file at `/home/user/rotation_report.json` containing the recovered old password, the extracted new password from the decrypted config, and the list of malicious IPs.

The final JSON file must strictly follow this exact schema:
```json
{
  "old_password": "<recovered_5_letter_password>",
  "new_password": "<extracted_new_password>",
  "malicious_ips": [
    "<ip_1>",
    "<ip_2>"
  ]
}
```
Sort the IPs in `malicious_ips` in ascending alphabetical/lexicographical order. Ensure your JSON is well-formed. Do not leave behind any unencrypted sensitive files.