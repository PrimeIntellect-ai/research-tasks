You are an artifact manager tasked with curating a repository of binary software packages. We recently discovered a vulnerability similar to "zip slip" in our system, where malicious actors uploaded packages with directory traversal sequences in the filenames to overwrite arbitrary files during extraction.

Your task is to write a C program that securely inspects these packages, combined with a shell command to locate the relevant files, and generate a curation report. 

The packages are located in `/home/user/artifacts/`.
You only need to process packages that meet BOTH of the following metadata criteria:
1. File extension is `.pkg`
2. File size is strictly less than 100 Kilobytes (100 KB).

**Package Format (`.pkg`) Specification:**
Each valid package contains a single record formatted strictly as follows:
- Magic Bytes: `4` bytes exactly matching `PKG1`
- Path Length (`N`): `1` byte (unsigned 8-bit integer) specifying the length of the filename
- Path: `N` bytes representing the destination filename
- GZ Size (`S`): `4` bytes (unsigned 32-bit integer, little-endian)
- GZ Data: `S` bytes of a gzip-compressed payload. When decompressed, this payload is a standard ELF binary.

**Execution Requirements:**
1. Write a C program at `/home/user/curate.c` that takes a `.pkg` file path as a command-line argument.
2. The program must read the package. 
3. If the embedded `Path` contains the substring `../`, the program should immediately flag it as a directory traversal attempt without processing the payload.
4. If the `Path` is safe, the program must decompress the `GZ Data` (using `zlib` in C) just enough to parse the ELF header of the uncompressed payload. You must extract the `e_machine` field (Architecture) from the ELF header, which is located at offset `0x12` (2 bytes, little-endian).
5. The program should output exactly one line to `stdout` per file:
   - For malicious paths: `[REJECT] <path> (Path Traversal)`
   - For safe paths: `[ACCEPT] <path> (Arch: 0x<e_machine_hex>)` 
     *(Format the architecture hex value in lowercase, e.g., `0x3e` or `0x3`)*
6. Use shell commands to find the relevant `.pkg` files based on the metadata criteria, pass them to your compiled C program, and redirect the sorted output to `/home/user/curation_report.txt`. The final file must be sorted alphabetically by the entire output string.

Ensure your C code compiles cleanly with `gcc /home/user/curate.c -o /home/user/curate -lz`.