You are a forensics analyst investigating a compromised host. We have recovered a suspicious audio file `/app/evidence.wav` from the machine. We suspect the attacker used this file to exfiltrate data via audio steganography or simple modulation (e.g., FSK or DTMF) combined with a cryptographic hash.

Your task is to:
1. Analyze `/app/evidence.wav` to extract the hidden payload. The payload consists of a sequence of encoded ASCII characters followed by a SHA-256 checksum of those characters.
2. Write a C++ program at `/home/user/decoder.cpp` that takes the raw extracted data as input, decodes the payload, and verifies the SHA-256 checksum.
3. If the checksum matches, your C++ program must output the decoded string and the time it took to verify, but more importantly, it must calculate the Shannon entropy of the decoded string.
4. Output the Shannon entropy value as a floating-point number to `/home/user/entropy.txt`.

We will evaluate your C++ program based on its accuracy in computing the entropy. You must ensure your entropy calculation is precise.