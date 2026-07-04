You are a DevSecOps engineer enforcing policy as code. Your task is to write a custom vulnerability and policy scanner in C++ that checks source files for security issues.

Write a C++ program at `/home/user/policy_scanner.cpp` and compile it to `/home/user/policy_scanner`.
The program should take a single command-line argument: the path to a directory to scan.
It must read all files in the given directory (you only need to handle a flat directory, no subdirectories) and check for the following vulnerabilities line by line:

1. **Insecure JWT Tokens**: Look for lines that start exactly with `jwt=`. The rest of the line is a JWT. You must base64url-decode the JWT header (the part before the first dot). If the decoded JSON header contains `"alg":"none"` (ignoring whitespace is not necessary, assume exact match of `"alg":"none"` or `"alg": "none"` if you do simple string matching, but actually you should just check if the decoded string contains `"none"` in the algorithm field), log a vulnerability.
2. **Weak Passwords**: Look for lines that start exactly with `custom_hash=`. The rest of the line is an integer representing a password hash. The hashing algorithm is defined as: the sum of the ASCII values of all characters in the plaintext password, modulo 256. You must read `/home/user/wordlist.txt`, hash each word using this algorithm, and if a match is found, log a vulnerability with the cracked plaintext.
3. **Deprecated SSH Keys**: Look for lines that start exactly with `ssh-dss `. This indicates a deprecated DSA key. Log a vulnerability.

When vulnerabilities are found, your program must append them to `/home/user/scan_report.log` in the following exact format:
`VULNERABILITY: JWT with alg=none found in <filename>`
`VULNERABILITY: Weak password <plaintext> found in <filename>`
`VULNERABILITY: Deprecated SSH key (ssh-dss) found in <filename>`

Sort the output lines in `/home/user/scan_report.log` alphabetically by filename. If there are multiple vulnerabilities in the same file, their relative order does not matter as long as they are grouped by filename.

Finally, run your compiled scanner on the directory `/home/user/repo`.

Notes:
- You may use standard C++ libraries only (no external dependencies like libssl or libcurl).
- The JWT header base64url decoding must be implemented or handled by your C++ code. You can assume the base64url string doesn't have padding.