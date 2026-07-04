You are a backup administrator tasked with recovering data from an old, proprietary archiving system. The data is stored in several binary archive files in the `/home/user/archives/` directory. Your goal is to write a C program that can parse these archive files, decompress the payloads, convert the text encoding to UTF-8, and extract the original files to `/home/user/extracted/`.

### Archive Format Specification
Each archive file has the following binary structure:

1.  **Magic Number:** 4 bytes, always `BKP1` (ASCII).
2.  **Filename Length:** 1 byte, unsigned integer indicating the length of the filename ($N$).
3.  **Filename:** $N$ bytes, ASCII characters representing the original filename.
4.  **Original Uncompressed Size:** 4 bytes, unsigned integer (little-endian), representing the size of the payload after decompression and before encoding conversion.
5.  **Compressed Payload Size:** 4 bytes, unsigned integer (little-endian), representing the size of the compressed data in the archive.
6.  **Encoding Flag:** 1 byte (always `0x02` for this dataset, meaning the original uncompressed text is in ISO-8859-1 encoding).
7.  **Payload:** The compressed binary payload using a custom Run-Length Encoding (RLE).

### RLE Decompression Rules
The payload is compressed using byte-pair RLE.
- The compressed payload consists of pairs of bytes: `[Count][Value]`
- `[Count]` is an unsigned 8-bit integer specifying how many times the `[Value]` byte should be repeated.
- For example, the hex sequence `0x04 0x41 0x01 0x42` expands to `AAAAB` (4 'A's, 1 'B').

### Encoding Conversion
Once decompressed, the bytes represent text in the ISO-8859-1 character set. You must convert this text to UTF-8 before saving it. 
*Hint:* In ISO-8859-1, characters `0x00`-`0x7F` are identical to ASCII/UTF-8. Characters `0x80`-`0xFF` translate to a two-byte UTF-8 sequence: `0xC2` or `0xC3` followed by a byte. Specifically, an ISO-8859-1 byte `ch` is converted to:
- `0xC2`, `ch` (if `ch` is `0x80` to `0xBF`)
- `0xC3`, `ch - 0x40` (if `ch` is `0xC0` to `0xFF`)

### Requirements
1.  Write a C program (e.g., `extractor.c`) to process all `.bkp` files found in `/home/user/archives/`.
2.  Compile the program using `gcc`.
3.  Run the program to extract all files into `/home/user/extracted/`.
4.  After extraction, create a summary log file at `/home/user/extraction_log.txt`. The log file must contain one line per extracted file in the format:
    `[Filename] successfully extracted. Final UTF-8 size: [Size] bytes`
    (Replace `[Filename]` with the exact filename from the header, and `[Size]` with the final byte count of the UTF-8 file written to disk). Sort the lines alphabetically by filename.

Please complete this task using standard CLI tools and standard C library functions.