You are tasked with building a custom configuration snapshot tool in Rust for a server environment. The system has various configuration files scattered in a directory structure. We need to back them up using a specific custom compression algorithm and ensure that the backup files are written atomically to prevent corruption.

Write and execute a Rust program (save it as `/home/user/snapshotter.rs` and compile it) that does the following:

1. **Recursive Traversal:** Recursively traverse the directory `/home/user/sys_config/`.
2. **File Filtering:** Process only files that have the `.cfg` extension.
3. **Custom Compression (Byte-level RLE):** Read the contents of each `.cfg` file and compress it using a custom Run-Length Encoding (RLE) algorithm. 
   - The RLE format should store pairs of bytes: `[count, byte]`.
   - `count` is a single `u8` representing the number of consecutive occurrences of the `byte`.
   - The maximum value for `count` is 255. If a byte repeats more than 255 times, output the pair `[255, byte]`, and then start a new pair for the remaining bytes.
   - Example: 3 bytes of 'A' (`0x41`) becomes `[0x03, 0x41]`.
4. **Atomic Writes:** Save the compressed data into `/home/user/snapshots/`. 
   - The original relative directory structure must be preserved. For example, `/home/user/sys_config/network/main.cfg` should be saved to `/home/user/snapshots/network/main.cfg.rle`.
   - You must create any missing subdirectories in `/home/user/snapshots/`.
   - **Crucial:** To ensure atomic writes, you must first write the compressed data to a temporary file named `<filename>.cfg.rle.tmp` in the target destination directory, and then atomically rename it to `<filename>.cfg.rle` (using `std::fs::rename`).
5. **Logging:** Keep track of the operation and generate a summary log file at `/home/user/snapshot_log.txt`. 
   - Each line in the log must be formatted exactly as: `<relative_path> -> <compressed_size_in_bytes> bytes`
   - Sort the lines alphabetically by `<relative_path>`.
   - Example line: `network/main.cfg -> 12 bytes`

Once you have written and compiled the Rust program, run it so that the snapshots and the log file are generated.