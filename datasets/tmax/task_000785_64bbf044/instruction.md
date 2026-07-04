You are an AI assistant helping a technical writer recover and organize documentation drafts. The writer's legacy documentation system is failing. It uses a custom Write-Ahead Log (WAL) format to stream edits, but a broken log rotation script is causing files to be copied while they are still being written to, resulting in trailing garbage bytes.

Your task is to write a C program to parse these WAL files, decode the text, apply a custom compression scheme, and write a bash script to process the entire directory and generate a manifest.

### The WAL Format Specification
1. **Magic Header:** Every valid WAL file starts with the 4 bytes `DOCW` (ASCII).
2. **Records:** The header is followed by a sequence of records. Each record starts with a 1-byte opcode:
   - `0x01` (Insert): Followed by a 2-byte unsigned little-endian integer `L` (length), then `L` bytes of payload data. These payload bytes must be appended to the current document buffer.
   - `0x02` (Delete): Followed by a 2-byte unsigned little-endian integer `C` (count). You must remove the last `C` characters from the current document buffer.
   - `0xFF` (Commit/End): Signifies the end of valid document operations. **You must stop reading the file immediately when this opcode is encountered.** Any bytes following `0xFF` are trailing garbage from the broken log rotation and must be completely ignored.
3. **Encoding:** The legacy system obfuscated the payload data. Every byte in the payload of an Insert (`0x01`) record is XOR'ed with `0xAA`. You must XOR each payload byte with `0xAA` to recover the original ASCII text before applying any deletes or compression.

### Custom Compression Specification (RLE)
After reconstructing the complete decoded text from a WAL file (stopping at `0xFF`), you must compress it using a specific Run-Length Encoding (RLE) format before saving it to disk:
- Iterate through the decoded text.
- If a character is repeated **4 or more** consecutive times (up to a maximum of 255 times), replace the sequence with three bytes:
  1. The Escape byte: `0x1B`
  2. The character itself.
  3. The count (as a single byte). For example, if 'A' appears 5 times, write `0x1B 0x41 0x05`.
- If a sequence exceeds 255 consecutive identical characters, start a new sequence.
- If a character repeats 3 or fewer times, write the characters as-is (uncompressed).
- You may assume the Escape byte (`0x1B`) never naturally occurs in the decoded text.

### Directory Structure and Processing Requirements
The raw WAL files are scattered inside the directory `/home/user/docs_raw/` (which may contain subdirectories).

1. Write a C program (e.g., `wal_parser.c`) that implements the parsing, decoding, and compression logic described above. It should take an input WAL file and output an RLE compressed file.
2. Compile the C program using `gcc`.
3. Create the output directory `/home/user/docs_processed/`.
4. Write and execute a bash script that:
   - Recursively finds all files ending in `.wal` within `/home/user/docs_raw/`.
   - Uses your compiled C program to process each `.wal` file.
   - Saves the compressed output into `/home/user/docs_processed/`. The output files must have the same base name as the original but with a `.rle` extension (flattening the directory structure; e.g., `/home/user/docs_raw/drafts/doc1.wal` becomes `/home/user/docs_processed/doc1.rle`). You can assume all base filenames are unique.
5. Finally, the bash script must generate a manifest file at `/home/user/docs_processed/manifest.txt` containing the `sha256sum` of every `.rle` file. The manifest must be sorted alphabetically by the `.rle` filename. Standard `sha256sum <file>` output format is required (hash followed by filename). When generating the manifest, run `sha256sum *.rle > manifest.txt` from within the `/home/user/docs_processed/` directory so that paths in the manifest are just the filenames.

Ensure all requirements are strictly met. The final verification will check the contents of `/home/user/docs_processed/manifest.txt` and the compressed `.rle` files.