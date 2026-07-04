You are a network engineer analyzing suspicious traffic caught on a local network segment. 

An unauthorized service was found intercepting traffic, and a captured payload from this service has been saved to `/home/user/dump.hex`. The payload is a hex-encoded string that has been encrypted using a simple single-byte XOR cipher to evade basic IDS pattern matching.

Your task is to:
1. Write a C program at `/home/user/decrypt.c` and compile it to `/home/user/decrypt`.
2. The program must read the hex-encoded payload from `/home/user/dump.hex`, brute-force the 1-byte XOR key, and decrypt the payload. You know for a fact that the decrypted plaintext contains the exact substring `MALWARE`.
3. Extract the IPv4 address of the attacker from the decrypted plaintext (it will be the only IP address in the string).
4. Save the extracted IP address to a file located at `/home/user/attacker_ip.txt`. The file should contain *only* the IP address.
5. To secure the service that was compromised, generate a 2048-bit RSA self-signed TLS certificate and private key. Save them as `/home/user/cert.pem` and `/home/user/key.pem`, respectively. The certificate must be valid for 365 days, and the Common Name (CN) must be exactly `secure-service`.

Ensure your C program handles the hex decoding and XOR brute-forcing autonomously. You may use standard C libraries.