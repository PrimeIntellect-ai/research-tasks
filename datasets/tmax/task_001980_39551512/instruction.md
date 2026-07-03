As a backup administrator, I need you to recover metadata from a corrupted legacy archive system. The archive is stored in a proprietary binary format, and I need a reliable way to extract the metadata, clean it up, and prepare it for our new system.

Here are your instructions:

1. Write a C program at `/home/user/extract_metadata.c` that parses a binary archive file located at `/home/user/legacy_archive.bin`.
   - For performance reasons, your C program MUST use memory-mapped I/O (`mmap`) to read the binary file.
   - The binary file contains a sequence of records. Each record has a 12-byte header followed by a variable-length payload.
   - Header format (little-endian 32-bit unsigned integers):
     - `Magic` (4 bytes): Always `0xBACCBACC`
     - `Type` (4 bytes): `1` for Data, `2` for Metadata
     - `Length` (4 bytes): The size of the payload in bytes (N).
   - Payload: N bytes of data immediately following the header.
   - Your C program must find all records of Type `2` (Metadata). The payload for these records is ASCII text (not null-terminated).
   - Write the extracted text payloads to `/home/user/raw_metadata.txt`, adding a newline (`\n`) after each payload. Ignore records of Type `1`.
   - Compile your program to `/home/user/extract_metadata` and run it.

2. The extracted metadata in `/home/user/raw_metadata.txt` will look like this: `ID:XXXX|DATE:YYYYMMDD|STATUS:Z`. 
   Use text processing tools (like `awk` or `sed`) to transform this file into a standard CSV format: `XXXX,YYYYMMDD,Z`. 
   Save the transformed output to `/home/user/clean_metadata.csv`.

3. Finally, generate a SHA-256 checksum manifest of the cleaned CSV file. 
   Save the output of the checksum command to `/home/user/manifest.txt` (the output format should exactly match standard `sha256sum`, e.g., `<hash>  clean_metadata.csv`). 
   Run the checksum command from inside the `/home/user/` directory so the path in the manifest is just the filename.

Ensure all final files (`raw_metadata.txt`, `clean_metadata.csv`, `manifest.txt`) are correctly formatted and placed in `/home/user/`.