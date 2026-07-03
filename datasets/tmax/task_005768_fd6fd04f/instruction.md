You are a penetration tester analyzing a custom beaconing tool found on a compromised host. 

You have been provided with two files in your home directory (`/home/user`):
1. `/home/user/malware.bin`: The ELF executable of the beacon.
2. `/home/user/payload.enc`: An encrypted payload capture that the beacon was attempting to exfiltrate.

Your analysis objectives are as follows:

**Phase 1: Binary Analysis**
The author of the malware hid the encryption key in a custom ELF section. Analyze `/home/user/malware.bin` and extract the raw bytes from the section named `.malware_key`. This is a repeating multi-byte XOR key.

**Phase 2: Decryption & Tooling**
Write a Go program at `/home/user/analyze.go`. This program must:
1. Read the encrypted `/home/user/payload.enc`.
2. Decrypt the payload using the XOR key you extracted from the binary. 
3. The decrypted payload is a plaintext file containing multiple raw, concatenated HTTP/1.1 requests.

**Phase 3: HTTP Header Inspection**
Enhance your Go program to parse the decrypted HTTP requests and inspect their headers. The malware communicates using a specific authentication token.
Find all occurrences of the `X-Beacon-Auth` HTTP header and extract its value.

**Phase 4: Reporting**
Your Go program should output the extracted authentication tokens to a file located at `/home/user/loot.txt`.
Write exactly one token per line in the order they appear in the decrypted traffic. Do not include the header name, only the value.

Ensure your script is self-contained and runs successfully via `go run /home/user/analyze.go`.