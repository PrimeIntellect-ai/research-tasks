You are a penetration tester who has intercepted a file containing proprietary command-and-control (C2) heartbeat payloads. 

The intercepted payloads are stored in `/home/user/intercepted_payloads.txt`. Each line in this file is a C2 instruction that has been obfuscated. 

Through earlier analysis, we know the obfuscation method:
1. The plaintext is first XOR-encrypted using a single-byte key: `0x2B`.
2. The resulting bytes are then Hex-encoded (uppercase or lowercase).

The underlying plaintext follows a strict delimiter format, for example:
`CMD:SCAN|TARGET_IP:10.0.0.5|USER:root|PASS:toor|ACTION:PING`

Your task is to write a C++ program at `/home/user/analyze_payloads.cpp` that does the following:
1. Reads the payloads from `/home/user/intercepted_payloads.txt`.
2. Decodes the Hex string to raw bytes.
3. Decrypts the raw bytes using the XOR key `0x2B` to recover the plaintext.
4. Redacts sensitive information from the plaintext to safely include it in our final pentest report. Specifically, you must replace the values of the `TARGET_IP`, `USER`, and `PASS` fields with the exact string `[REDACTED]`.
5. Writes the final redacted plaintexts to `/home/user/redacted_payloads.log`, with one payload per line in the same order as the input.

For example, if the decrypted plaintext is `CMD:EXEC|TARGET_IP:192.168.1.1|USER:admin|PASS:secret|ACTION:DROP`, the output written to the log must be exactly:
`CMD:EXEC|TARGET_IP:[REDACTED]|USER:[REDACTED]|PASS:[REDACTED]|ACTION:DROP`

Compile and run your C++ code so that `/home/user/redacted_payloads.log` is generated successfully.