You are a forensics analyst investigating a recently compromised Linux server. 

During the investigation, you recovered a suspicious, stripped executable located at `/app/c2_encoder`. Analysis of network logs indicates that the attacker used this binary to encode sensitive files before exfiltrating them via a covert command-and-control (C2) channel. We have captured a large number of file transfers from the network, but the attacker mixed their encoded exfiltration payloads with benign, encrypted traffic to evade detection.

Your goal is to reverse engineer the attacker's custom encoding tool and build an automated classifier to detect the exfiltrated payloads.

**Task Instructions:**
1. **Reverse Engineering:** Analyze the stripped binary `/app/c2_encoder`. Determine the custom cryptographic algorithm it uses to encode data. Pay close attention to how it manipulates bytes and if it appends any metadata or checksums to the encoded output. Standard reverse engineering tools (like `objdump`, `strings`, `gdb`, `strace`, etc.) are available on the system.
2. **Detector Implementation:** Write a classifier in C that can statically identify whether a given file was encoded by `/app/c2_encoder`.
   - Your source code must be saved at `/home/user/detector.c`.
   - Compile it to an executable at `/home/user/detector`.
   - The executable must accept exactly one argument: the absolute path to a file to inspect. E.g., `./detector /path/to/file`.
   - The program must exit with status code `1` (Reject/Evil) if the file contains a valid payload encoded by the attacker's tool.
   - The program must exit with status code `0` (Accept/Clean) if the file is benign and does not match the encoding tool's exact algorithmic footprint.

**Data Corpora:**
We have provided two directories of captured files to help you test your detector:
- `/home/user/corpus/evil/`: Contains 50 files that are known to be encoded by `/app/c2_encoder`.
- `/home/user/corpus/clean/`: Contains 50 benign files (random encrypted traffic, normal system files, etc.) that were not processed by the tool.

Your detector must achieve 100% accuracy. It must correctly return exit code 1 for every file in the `evil` corpus, and exit code 0 for every file in the `clean` corpus.