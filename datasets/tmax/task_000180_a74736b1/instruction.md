You are a forensics analyst investigating a compromised Linux host. A suspicious hidden process has been isolated and is currently running a local HTTP command-and-control (C2) interface on a high port (between 8000 and 9000) bound to 127.0.0.1. 

Your objective is to recover the attacker's 6-digit evidence lock PIN.

Perform the following steps:
1. Identify the port the suspicious HTTP service is listening on.
2. Query the root path (`/`) of this service and inspect the HTTP response headers and cookies.
3. The service responds with a custom header `X-Malware-Salt` containing a 4-character salt, and sets a cookie named `Evidence-Token`. This token is the MD5 hash of the attacker's 6-digit numeric PIN concatenated with the salt (Format: `MD5(PIN + Salt)`). The PIN is exactly 6 digits, zero-padded (e.g., 000000 to 999999).
4. Write a C++ program at `/home/user/bruteforce.cpp` that programmatically brute-forces the 6-digit PIN. You may use OpenSSL (`<openssl/md5.h>`) for the MD5 hashing. Compile it and run it to discover the PIN.
5. Once you have successfully recovered the 6-digit PIN, save it to a file exactly at `/home/user/recovered_pin.txt`. The file should contain nothing but the 6-digit PIN.
6. To maintain forensic integrity, change the file permissions of `/home/user/recovered_pin.txt` to strictly read-only for the owner (0400), with no permissions for group or others.

Note: You have `sudo` access if package installation (like `libssl-dev`) is necessary, but standard execution does not require root. Use standard C++17 or earlier. Compile using `g++`.