You are a forensics analyst investigating a recent server compromise. We have captured an application-layer network log from the breached host. You must analyze the log, identify the exfiltrated data, and write a C++ program to decode and decrypt it.

The log file is located at `/home/user/evidence/network_log.txt`. 

Log Format:
`[SRC_IP] [DST_IP] [DST_PORT] [ACTION] [DATA]`

Your task consists of the following phases:
1. **Log Analysis**: The attacker's IP is `192.168.1.100`. Examine the log to find the attacker's successful authentication event (`ACTION: AUTH_SUCCESS`). The `DATA` field for this event contains their authentication token.
2. **Payload Extraction**: The attacker exfiltrated data using the action `EXFIL`. The `DATA` fields for these events contain hex-encoded chunks of the encrypted payload. Combine these chunks in the order they appear to form the complete hex-encoded ciphertext.
3. **Decryption Tool**: Write a C++ program at `/home/user/decoder.cpp` that performs the following:
   - Takes the hex-encoded ciphertext and decodes it into raw bytes.
   - Decrypts the raw bytes using a repeating byte-wise XOR cipher, where the decryption key is the authentication token found in step 1.
   - Outputs the plaintext string.
4. **Execution**: Compile your C++ program to `/home/user/decoder` and run it. Save the final, decrypted plaintext to `/home/user/evidence/decrypted_secret.txt`.

Ensure your C++ program is self-contained and handles the hex decoding and XOR logic accurately.