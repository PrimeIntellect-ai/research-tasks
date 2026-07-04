You are acting as an incident responder investigating a breach at our video streaming subsidiary. Attackers managed to exfiltrate an encryption key via a steganographic broadcast and are now using it to send encrypted malicious payloads to our backend API. 

We have captured a recording of the compromised broadcast stream and saved it at `/app/evidence.mp4`. We also have two directories containing intercepted web request payloads: `/app/corpus/clean/` (legitimate user traffic) and `/app/corpus/evil/` (malicious traffic from the attackers).

Your task is to:
1. Extract the hidden encryption key from `/app/evidence.mp4`. The key was briefly flashed on screen encoded in base64 format between seconds 12 and 15 of the video.
2. Once you have the key, write a C++ program at `/home/user/payload_filter.cpp` that acts as a secure payload filter.
3. The C++ program must accept a single command-line argument (the path to a payload file). It must decode the payload, attempt to decrypt it using the key you found, and determine if it is malicious.
4. Malicious payloads contain the string `EXEC_SHELL` or attempt path traversal (`../`) after decryption. Legitimate payloads do not.
5. Compile your program to `/home/user/filter_bin`.
6. Your program must exit with status code 0 if the payload is clean, and exit with status code 1 if the payload is malicious.
7. Set the permissions of `/home/user/filter_bin` to `755`.

You must ensure your filter correctly identifies all clean payloads as clean and all evil payloads as evil.