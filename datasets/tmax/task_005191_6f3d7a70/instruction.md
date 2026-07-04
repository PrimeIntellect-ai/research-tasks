You are acting as an artifact manager curating a binary repository. You need to process a directory of artifacts, split the large files to avoid size limits, compress the chunks, and generate a manifest.

Your task is to write and execute a bash script (using standard coreutils and built-ins) that does the following:
1. Recursively traverse the directory `/home/user/repo`.
2. Find all files that are strictly larger than 1,000,000 bytes.
3. For each of these large files:
   - Compute its SHA-256 hash.
   - Split the file into chunks of exactly 500,000 bytes. Use a numeric suffix for the chunks starting from `00`, with the naming format: `[original_filename].part[suffix]` (e.g., `app.bin.part00`, `app.bin.part01`).
   - Compress each generated chunk using `gzip` (this will append `.gz` to the chunk filenames).
   - Delete the original large file.
4. Create a manifest file at `/home/user/manifest.txt`. For each large file that was processed, append a line with the following format:
   `<absolute_path_to_original_file>|<number_of_chunks_generated>|<sha256_hash_of_original_file>`
   (e.g., `/home/user/repo/app.bin|5|e3b0c442...`)
5. The lines in `/home/user/manifest.txt` must be sorted alphabetically by the absolute path of the original file.

Small files (1,000,000 bytes or smaller) should be completely ignored and left as they are.

Ensure your script handles paths and filenames correctly and leaves the properly named compressed chunks in the exact same directory where the original file was located.