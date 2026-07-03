You are a storage administrator managing disk space for a video processing pipeline. Your system uses a custom compression format for raw video frames, but some storage nodes have been corrupted, producing malformed or malicious files (e.g., RLE bombs that exhaust memory, or files with truncated data).

You need to write a Python script `/home/user/storage_manager.py` that filters a directory of these custom-compressed frames, rejects the corrupted/malicious ones, and securely decompresses and deduplicates the valid ones.

### The Custom Frame Format (`.frm1`)
Each valid file is a binary file with the following structure:
1. **Magic Header** (4 bytes): The ASCII string `FRM1`.
2. **Original Size** (8 bytes, little-endian unsigned integer): Must be exactly `6220800` (which corresponds to 1920x1080x3 bytes for a 1080p RGB frame).
3. **Compressed Size** (8 bytes, little-endian unsigned integer): Must exactly match the number of remaining bytes in the file.
4. **Data**: Run-Length Encoded (RLE) bytes. The RLE format consists of pairs of bytes: `[count][value]`. 
   - `count` is an unsigned 8-bit integer (1-255). `count = 0` is illegal.
   - `value` is the byte value to repeat `count` times.
   - The total decompressed size of the RLE data must exactly equal the Original Size.

### Task Requirements
Your script will be invoked as:
`python3 /home/user/storage_manager.py <input_dir> <output_dir>`

It must iterate over all files ending in `.frm1` in `<input_dir>`. 
For each file:
1. **Validate**: Check the magic bytes, sizes, and RLE integrity. Read efficiently (e.g., using memory-mapped I/O or streaming). Do NOT read the whole file into memory before validating the headers, as malicious files may claim massive sizes. If a file violates ANY of the format rules, **ignore it completely** (do not write any output for it).
2. **Decompress**: Decode the valid RLE data.
3. **Deduplicate (Hard Links)**: Hash the uncompressed raw bytes using SHA-256. Save the raw bytes to `<output_dir>/objects/<sha256_hex>.raw`. If a file with this hash already exists in the `objects` directory, you **must use a hard link** to the existing file to save disk space, instead of writing a new file.
4. **Sequence (Symlinks)**: Create a symbolic link at `<output_dir>/sequence/<original_filename_without_extension>.raw` that points to the corresponding hard-linked file in the `objects` directory.

### Corpora & Testing
There is a reference video at `/app/reference_video.mp4` you can use to generate test data using `ffmpeg` and your own encoding script.
However, your final script will be tested against two hidden corpora:
- A "clean" corpus containing valid frames (with duplicates).
- An "evil" corpus containing maliciously constructed files (size mismatches, bad magic, RLE bombs, illegal zero-counts).

Your script must perfectly isolate the clean frames and completely reject the evil ones.