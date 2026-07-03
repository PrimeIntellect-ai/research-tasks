You are helping a researcher organize a massive, messy dataset of audio recordings. The dataset is located at `/app/dataset`. Over the years, automated scripts have created recursive symlinks within this directory, resulting in infinite loops (e.g., a `backup` folder symlinked to its own parent).

You need to write a standalone Python tool, `/home/user/pack_audio.py`, that safely traverses directories, custom-compresses `.wav` files, and packages them into a single archive format with integrity verification.

Your script must implement the following Command Line Interface:
1. `python3 /home/user/pack_audio.py pack <input_dir> <output_file.car>`
2. `python3 /home/user/pack_audio.py verify <input_file.car>`

### Archiving and Traversal Rules (`pack`)
- Recursively find all files ending in `.wav` inside `<input_dir>`.
- **Symlink Loops:** You must follow symlinks to directories, but to prevent infinite loops, you must **skip** any directory whose resolved absolute path has already been visited during the traversal.
- Compute the relative path of each `.wav` file from `<input_dir>` (e.g., `recordings/sample.wav`). Use forward slashes `/` for paths.
- Sort these relative paths in strict alphabetical order. Process the files in this sorted order.

### Custom Compression
For each file, read its raw bytes and compress them using a custom Byte-Level Run-Length Encoding (RLE):
- Sequences of identical bytes are encoded as two bytes: `[Count][ByteValue]`.
- `Count` is an unsigned 8-bit integer (1 to 255).
- If a byte repeats more than 255 times, encode the first 255 as `[255][ByteValue]`, then continue encoding the remainder.
- Example: `b"AAAAABBB"` (5 A's, 3 B's) becomes `b"\x05A\x03B"`.

### Binary Archive Format (`.car`)
The output archive must be written exactly as follows:
1. **Magic Header:** The exact 9 bytes `b"AUDIOCAR\x00"`.
2. **File Entries:** For each `.wav` file (in the alphabetically sorted relative path order), write:
   - **Path Length:** 2 bytes, little-endian unsigned integer representing the length of the UTF-8 encoded relative path.
   - **Relative Path:** The UTF-8 encoded relative path string.
   - **Uncompressed Size:** 4 bytes, little-endian unsigned integer.
   - **Compressed Size:** 4 bytes, little-endian unsigned integer.
   - **Compressed Data:** The RLE-compressed bytes of the file.
3. **Footer / Integrity Check:**
   - Compute the standard CRC32 (as calculated by `zlib.crc32`) of all bytes written to the archive *so far* (from the magic header up to the end of the last file's compressed data).
   - Write this CRC32 as a 4-byte little-endian unsigned integer at the very end of the file.

### Verification (`verify`)
When invoked with `verify <input_file.car>`, the script must:
- Read the archive.
- Recompute the CRC32 of the archive content (everything except the last 4 bytes).
- Compare it to the 4-byte CRC32 footer.
- If they match perfectly, print exactly `Archive OK` to standard output and exit with status code `0`.
- If they do not match, or if the file cannot be read/is malformed, print exactly `Archive Corrupted` to standard output and exit with status code `1`.

### Integration Step
Once your script is complete and tested, run it on the provided dataset to create the final archive:
`python3 /home/user/pack_audio.py pack /app/dataset /home/user/dataset.car`

Ensure the script is written robustly and does not crash on empty files or deep directories.