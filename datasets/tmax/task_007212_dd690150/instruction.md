You are a red-team operator simulating an attack against a custom Command and Control (C2) server to test its evasion and parsing capabilities. 

We have intercepted a log file from the target C2 server located at `/home/user/c2_logs.txt`. The log file contains timestamps, source IPs, and hex-encoded encrypted payloads.

Through previous reverse-engineering, we know the following about the C2 payload structure and encryption:
1. Every valid plaintext command starts with the header: `MAGIC_C2_REQ:`
2. The payload is encrypted using a custom rolling XOR stream cipher based on a Linear Congruential Generator (LCG).
3. The first byte of the raw binary payload (before hex encoding) is a randomly generated `seed` sent in plaintext.
4. The LCG generates the keystream using the formula: `key[i] = (key[i-1] * 13 + 11) % 256`, where `key[0] = seed`.
5. The plaintext is XORed with the keystream starting at `key[1]`. So, `ciphertext[1] = plaintext[0] XOR key[1]`, `ciphertext[2] = plaintext[1] XOR key[2]`, and so on.

Your task:
1. Write a Python script to parse the logs, verify the encryption logic, and craft a new encrypted payload.
2. The payload must decrypt to exactly the following plaintext string: `MAGIC_C2_REQ:CMD=whoami`
3. You must choose a random seed for your payload (any integer between 0 and 255).
4. Save the final crafted payload as a continuous hex string (no spaces or newlines) to the file `/home/user/payload.hex`.

Your script and manual commands are up to you, but the final deliverable must be the correctly formatted `/home/user/payload.hex` file.