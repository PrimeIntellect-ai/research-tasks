You are a forensics analyst recovering evidence from a compromised host. The attacker attempted to wipe the system logs, but we have recovered a raw binary data dump from memory, located at `/home/user/suspect_data.dat`.

Your task is to write a C program, `/home/user/parser.c`, that extracts valid log frames from the binary dump, redacts any sensitive API keys, and outputs the clean evidence. 

The binary file contains random garbage mixed with valid log frames. A valid log frame has the following strict structure:
1. **Magic Bytes**: Exactly two bytes `0xBE` followed by `0xEF`.
2. **Length**: A 2-byte unsigned integer (little-endian) representing the length of the payload (`L`). The length `L` will never exceed 1024 bytes.
3. **Payload**: Exactly `L` bytes of ASCII text.
4. **Checksum**: A 1-byte checksum immediately following the payload. The checksum is calculated as the bitwise XOR sum of all bytes in the **Payload** ONLY (not including the magic bytes or length).

Your C program must:
1. Read `/home/user/suspect_data.dat` and scan for valid frames. A frame is only valid if the magic bytes match, and the computed XOR checksum of the payload matches the checksum byte at the end of the frame.
2. For each valid frame's payload, search for the exact string `API_KEY=`. If found, and it is followed by exactly 16 alphanumeric characters (e.g., A-Z, a-z, 0-9), you must redact those 16 characters by replacing them with 16 asterisks (`*`). Do not modify any other part of the payload.
3. Print each valid, potentially redacted payload to standard output, followed by a newline (`\n`). If a payload already ends in a newline, do not print an extra one.

After verifying your C program works, compile it and run it to save the output to `/home/user/recovered_logs.txt`.

Finally, generate the SHA-256 hash of `/home/user/recovered_logs.txt` and save the standard `sha256sum` output to `/home/user/recovered_logs.sha256`.