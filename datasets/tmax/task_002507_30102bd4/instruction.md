You are a storage administrator tasked with reclaiming disk space on a legacy Linux server by archiving old, large files into cold storage. Standard compression algorithms are fine for binary data, but for legacy text logs, you must implement a specific custom compression algorithm as mandated by company policy.

Your task has several phases. All work should be done in `/home/user/`.

**Phase 1: Metadata-Based File Search**
Search the directory `/home/user/data_volume` for files that meet BOTH of the following criteria:
1. Modified strictly before `2023-01-01 00:00:00 UTC`.
2. Size is strictly greater than `10000` bytes.

**Phase 2: Custom Compression & Archiving**
You must package the files found in Phase 1 into a single uncompressed tar archive located at `/home/user/cold_storage.tar`. However, before adding them to the tarball, they must be individually compressed:
*   **Text Files (`.txt` extension):** You must write a Python script to compress these using a custom byte-level Run-Length Encoding (RLE). The RLE format consists of pairs of bytes: `[count][byte_value]`. 
    *   `count` is a single unsigned byte representing the number of repetitions (from 1 to 255).
    *   `byte_value` is the single byte being repeated.
    *   If a run exceeds 255 identical consecutive bytes, you must split it into multiple pairs (e.g., 260 bytes of `0x41` becomes `0xFF 0x41 0x05 0x41`).
    *   Store these files in the tarball with their original name but with `.rle` appended (e.g., `logs/app.txt` becomes `logs/app.txt.rle`).
*   **Other Files (any other extension):** Compress these using standard `gzip`. Store them in the tar archive with `.gz` appended (e.g., `dumps/core.bin` becomes `dumps/core.bin.gz`).

*Note: The paths inside the tarball should be relative to `/home/user/data_volume` (e.g., `file1.txt.rle`, not `home/user/data_volume/file1.txt.rle`).*

**Phase 3: Manifest Generation**
Create a manifest file at `/home/user/manifest.txt` documenting the archived files. Each line must be formatted exactly as follows:
`[relative_path_inside_data_volume] [sha256_hex_hash_of_original_UNCOMPRESSED_file]`
Sort the lines alphabetically by the relative path.

**Phase 4: Integrity Verification**
Write a Python script at `/home/user/verify.py`. This script must:
1. Open `/home/user/cold_storage.tar`.
2. Read the compressed files from the archive into memory.
3. Decompress them according to their extension (`.rle` custom decompression, `.gz` standard gzip).
4. Calculate the SHA-256 hash of the decompressed data.
5. Verify these hashes against `/home/user/manifest.txt`.
6. Print exactly `INTEGRITY_PASSED` to standard output and exit with code 0 if all files match perfectly. If there are any discrepancies, print an error and exit with a non-zero code.

You may use any bash commands or write any helper Python scripts you need to accomplish this task.