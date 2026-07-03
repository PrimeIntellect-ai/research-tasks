You are helping a developer organize and secure a new project file delivery system. The project uses a custom text-based "manifest" format to describe file chunks that need to be merged together. Recently, a security researcher pointed out that our automated extraction system is vulnerable to "zip slip" style directory traversal attacks, where a manifest might instruct the system to write files outside the target extraction directory.

Your task is to write a standalone C program that acts as a security filter for these manifest files. 

First, listen to the voicemail left by the lead engineer at `/app/voicemail.wav`. The voicemail contains a specific secret "magic header" string that every valid manifest must start with.

The manifest format is strictly text-based and follows this structure:
```
HEADER <magic_header_string>
FILE: <destination_path>
CHUNKS: <number_of_chunks>
CHECKSUM: <sha256_hash>
```
(A manifest may contain multiple FILE blocks).

You must write a C program at `/home/user/manifest_filter.c` and compile it to `/home/user/manifest_filter`. 

The program must take exactly one command-line argument: the path to a manifest file.
Usage: `./manifest_filter <path_to_manifest>`

Your program must read the file and enforce the following rules:
1. The first line must exactly match the `HEADER ` followed by the secret string you heard in the voicemail.
2. Every `FILE: ` path must be strictly relative. It must NOT be an absolute path (cannot start with `/`).
3. Every `FILE: ` path must NOT contain any directory traversal sequences (specifically, the substring `../`).
4. If the manifest perfectly adheres to all rules, your program must terminate with exit code `0` (accept).
5. If the manifest violates ANY of these rules (wrong header, absolute path, or traversal sequence), your program must terminate with exit code `1` (reject).

To help you test, there are two directories containing sample manifests:
- `/app/corpora/clean/`: Contains valid, safe manifests.
- `/app/corpora/evil/`: Contains malicious manifests (bad headers, absolute paths, or zip-slip attempts).

Your compiled program will be tested against a hidden set of clean and evil manifests. It must correctly accept all clean manifests and reject all evil manifests.