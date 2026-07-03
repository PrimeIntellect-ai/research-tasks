You are acting as a forensics analyst responding to a compromised Linux web server. The attacker exploited an open redirect vulnerability in the login flow to drop backdoored executables. 

We have recovered a screenshot of the attacker's terminal during the breach, located at `/app/attacker_console.png`. It contains the hexadecimal encryption key the attacker used to obfuscate the malicious payload injected into the backdoored files.

We have collected a corpus of executable files from the system. Some are legitimate web server binaries, and some are the attacker's modified backdoors.
The corpora are located at:
- Malicious: `/app/corpus/evil/`
- Legitimate: `/app/corpus/clean/`

The malicious binaries are ELF files that contain a hidden string `AUTH_BYPASS!` somewhere in their contents. To evade detection, the attacker obfuscated this string by XORing the entire file's binary content with a 32-bit key (the one visible in the screenshot). The XOR operation was applied to 32-bit aligned blocks (little-endian). Legitimate binaries do not contain this obfuscated string.

Your task is to build a malware detector in C++:
1. Inspect the image `/app/attacker_console.png` to recover the 32-bit XOR key (you may use `tesseract` or other available tools).
2. Write a C++ program at `/home/user/detector.cpp` that takes a file path as its first command-line argument.
3. The program must read the file, decrypt the contents using the XOR key (aligned to 4-byte boundaries), and search for the exact string `AUTH_BYPASS!`.
4. The program must output exactly `MALICIOUS` to standard output if the payload is found, or `CLEAN` if it is not found. Output a newline after the word.
5. Compile your program to `/home/user/detector`.

Requirements:
- Your program will be tested automatically against the `evil` and `clean` corpora. 
- It must accurately classify 100% of the files in both directories.
- Ensure your C++ code correctly handles file I/O and binary data. Do not alter the files in the corpus.