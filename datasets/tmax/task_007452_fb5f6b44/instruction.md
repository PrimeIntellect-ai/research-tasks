You are tasked with building a secure artifact extraction pipeline for a binary repository manager. 

A legacy system exports repository artifacts using a proprietary "Custom Artifact Format" (CAF) archive. These archives are piped between systems via standard streams. Recently, a security audit revealed that malicious actors are attempting "Zip Slip" directory traversal attacks by injecting paths like `../` or absolute paths (`/etc/...`) into these archives.

Your objective is to write a secure C program that extracts these archives, and a bash script that orchestrates the extraction and transforms the extracted metadata.

**Part 1: The Extractor (C)**
Write a C program at `/home/user/caf_extractor.c`. 
The program must process a CAF archive fed to it via **standard input (`stdin`)** and safely extract its contents to the current working directory.

The CAF format specification is as follows:
1. **Magic Header**: The first 4 bytes are exactly `CAF\x01`.
2. **Entries**: The rest of the file consists of consecutive file entries until EOF. Each entry contains:
   - `path_len`: 1 byte (unsigned integer) representing the length of the file path.
   - `path`: `path_len` bytes of ASCII text (no null terminator).
   - `compressed_size`: 4 bytes (unsigned integer, little-endian) representing the size of the compressed data payload.
   - `data`: `compressed_size` bytes of compressed data.

**Compression Algorithm**: The payload is compressed using a simple Run-Length Encoding (RLE). The compressed data consists of pairs of bytes: `[count][byte]`. For example, `\x03\x41` means `AAA`.

**Security Requirements**: 
- If a `path` begins with `/` or contains `../`, it is considered malicious.
- Your program MUST NOT extract malicious files. Instead, it must discard their payload and print a warning exactly in this format to **standard error (`stderr`)**: `WARNING: Skipped malicious path: <path>`
- Valid files should be decompressed and written to the current working directory using their provided filename. (You can assume valid files have flat names with no subdirectories).

**Part 2: The Processing Pipeline (Bash)**
There is a sample archive located at `/home/user/repo.caf`.
Write a shell script at `/home/user/process.sh` that performs the following steps:
1. Compiles `/home/user/caf_extractor.c` using `gcc`.
2. Creates an output directory at `/home/user/output` and navigates into it.
3. Uses standard input redirection to pipe `/home/user/repo.caf` into the compiled extractor.
4. One of the valid files safely extracted will be `artifacts.csv`. Parse this CSV file (which has a header `id,artifact_name,checksum`) and convert it into a strictly formatted JSON array.
5. Save the JSON array to `/home/user/output/summary.json`. 

The JSON should look exactly like this (whitespace matters for automated verification):
```json
[
  {
    "id": "1",
    "artifact_name": "kernel_mod",
    "checksum": "a1b2c3d4"
  },
...
]
```

Ensure your pipeline completes correctly and automatically when `/home/user/process.sh` is executed.