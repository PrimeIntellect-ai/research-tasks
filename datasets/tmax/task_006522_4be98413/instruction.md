As an incident responder, you are investigating a suspicious file upload handler found on a compromised Linux system. The attacker left behind a compiled binary at `/home/user/upload_handler` and its corresponding source code at `/home/user/upload_handler.c`. 

Upon reviewing the source code, you noticed it contains a buffer overflow vulnerability. When successfully exploited, the binary extracts a hidden log file to `/home/user/evidence.log`.

However, the binary expects the uploaded payload to be encrypted using a simple 1-byte XOR cipher (every byte of the payload is XORed with a single unknown byte value between 0x00 and 0xFF).

Your task:
1. Craft a payload that exploits the buffer overflow to overwrite the `isAdmin` variable with the exact hex value `0x1337BEEF` (taking little-endian architecture into account).
2. Since you do not know the 1-byte XOR key the attacker used, you must brute-force it. Write a script (in bash or C) to XOR your payload with all possible 256 keys, feeding each resulting file to `/home/user/upload_handler` until the `/home/user/evidence.log` file is successfully generated.
3. The generated `/home/user/evidence.log` contains sensitive user information, including IPv4 addresses. You must redact all IPv4 addresses in this file by replacing the first three octets with `XXX.XXX.XXX.`, keeping only the final octet (e.g., `192.168.1.42` becomes `XXX.XXX.XXX.42`). Save the fully redacted file to `/home/user/redacted_evidence.log`.

Do not modify the `upload_handler` binary itself. You have all standard Linux tools and a C compiler (gcc) available.

Verification will be based strictly on the presence and correct formatting of `/home/user/redacted_evidence.log`.