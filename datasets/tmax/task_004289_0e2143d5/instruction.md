I am a researcher dealing with a messy dataset of mixed file types spanning deep directory trees. I need you to write a Rust tool to organize these files and pack them into a custom archive format to save space and standardise my data pipeline.

The messy dataset is located in `/home/user/raw_data/` (this directory already exists and contains many files and subdirectories).

Your task is to create a Rust project in `/home/user/dataset_packer/` and write a binary that performs the following steps:

1. **Recursive Traversal & Classification:**
   Recursively traverse `/home/user/raw_data/`. For every file, determine its type by reading its first few bytes:
   - **ELF binary:** Starts with `0x7F 0x45 0x4C 0x46`
   - **SQLite WAL:** Starts with `0x37 0x7F 0x06 0x82` or `0x37 0x7F 0x06 0x83`
   - **GCode file:** Starts with the exact ASCII string `; FLAVOR:`
   Ignore any file that does not match one of these three signatures.

2. **Organization via Symlinks:**
   For each matched file, create a symbolic link in `/home/user/categorized/` under a subdirectory corresponding to its type (`elf/`, `wal/`, `gcode/`). 
   To avoid naming collisions, the symlink name must be the original filename prefixed with the SHA-256 hash of the *absolute original file path*, followed by an underscore.
   Example: If the original file is `/home/user/raw_data/sims/run1.elf`, the symlink should be `/home/user/categorized/elf/<hash_of_absolute_path>_run1.elf`.

3. **Custom Archiving (CPACK):**
   After creating all symlinks, your Rust program must pack the files into a single archive at `/home/user/dataset.cpack`. You must read through the symlinks in `/home/user/categorized/` (in lexicographical order of their relative paths, e.g., `elf/hash_a.elf`, `elf/hash_b.elf`, `gcode/hash_c.gcode`, etc.) and write them to the archive.
   
   **The `.cpack` File Format:**
   - **Header:** 8 bytes: `CPACK\0\0\0`
   - **File Entries** (repeated for each file):
     - `path_len`: 2 bytes (u16, Little Endian) - length of the relative path string.
     - `path`: UTF-8 string of the relative path (e.g., `elf/abc_run1.elf`).
     - `uncompressed_size`: 8 bytes (u64, Little Endian) - size of the uncompressed file data.
     - `compressed_data`: The file contents compressed using a Custom Run-Length Encoding (RLE).
   
   **Custom RLE Specification:**
   - The data is represented as pairs of bytes: `[count][value]`.
   - `count` is a 1-byte unsigned integer (1 to 255) representing how many times `value` is repeated.
   - If a byte repeats more than 255 times, you must split it into multiple pairs (e.g., 258 'A's becomes `[255]['A'][3]['A']`).
   - Even non-repeating bytes are encoded as pairs (e.g., a single 'B' is `[1]['B']`).

Run your Rust program to create the categorized directories, the symlinks, and the final `/home/user/dataset.cpack` file.