You are a network security engineer investigating a suspected data exfiltration incident. You have been provided with two pieces of evidence found on a compromised Linux gateway:
1. `/home/user/filter_engine` - A compiled C binary that processes raw network packet payloads. We suspect the attacker modified this tool to silently extract hidden messages from specific packets.
2. `/home/user/capture.hex` - A text file containing a hex dump of captured network payloads (one packet payload per line).

Your task is to:
1. Reverse engineer the `/home/user/filter_engine` binary using standard command-line tools (like `objdump`, `strings`, or `gdb`).
2. Identify the 4-byte magic signature (represented as 8 hex characters at the very beginning of a packet) that triggers the hidden backdoor logic.
3. Determine the cryptanalysis/decryption logic used by the backdoor on the remainder of the packet payload. (Hint: It uses a simple single-byte XOR operation).
4. Write a C program at `/home/user/decoder.c` that parses `/home/user/capture.hex`, searches for packets starting with the magic signature, extracts the hidden payload bytes, decrypts them using the identified algorithm, and prints the decrypted ASCII characters.
5. Compile your C program to `/home/user/decoder` and run it, redirecting its standard output to `/home/user/secret.txt`.

Ensure your C program is robust enough to ignore normal traffic in the hex file and only process the backdoored packets. The final extracted string in `/home/user/secret.txt` should contain the cleartext exfiltrated message.