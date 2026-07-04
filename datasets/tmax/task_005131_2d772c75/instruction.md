You are acting as a penetration tester analyzing a leaked dataset from a compromised web server. The server suffered from an open redirect vulnerability combined with a weak custom authentication hashing mechanism.

You have been provided with the following files in the `/home/user/` directory:
1. `/home/user/auth_logs.txt`: A log file containing intercepted login attempts. Each line is formatted as: 
   `[TIMESTAMP] user=<username> redirect_payload=<base64_encoded_url> hash=<hex_hash_value>`
2. `/home/user/wordlist.txt`: A dictionary of potential passwords.
3. `/home/user/custom_hash.h`: A C++ header file containing the proprietary hashing function used by the server: `unsigned int compute_hash(const std::string& password);`
4. `/home/user/ssh_key_backup`: A sensitive key file left with overly permissive permissions.

Your task is to write a C++ program named `/home/user/cracker.cpp` that does the following:
1. Reads `/home/user/auth_logs.txt`.
2. Decodes the base64 `redirect_payload` for each entry.
3. Uses the provided `/home/user/wordlist.txt` to brute-force the password for each entry by hashing each word using `compute_hash` from `custom_hash.h` and comparing it to the hex `hash` value in the log.
4. Outputs the successfully cracked accounts to `/home/user/compromised_accounts.txt` in the exact following format, one per line:
   `username:cracked_password:decoded_redirect_url`

Additionally, you must secure the sensitive key file by changing the permissions of `/home/user/ssh_key_backup` to read-only for the owner (and no access for anyone else).

Constraints:
- You must write the solution in C++ (`/home/user/cracker.cpp`) and compile it using standard `g++`.
- Do not use external libraries for base64 decoding; implement a simple base64 decoder in your C++ code or rely on standard C++ tools. 
- Ensure the final output file `/home/user/compromised_accounts.txt` is created with the exact format specified.