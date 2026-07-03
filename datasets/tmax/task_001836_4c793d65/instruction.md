You are helping a researcher organize a large collection of sensor dataset archives. The datasets are stored in a custom binary format in the `/home/user/archives/` directory.

Each `.dat` file in this directory consists of two parts:
1. An 8-byte ASCII string representing the format version (either `DATAv1.0` or `DATAv2.0`).
2. A raw gzipped stream of text data immediately following the 8-byte header.

Your task is to write and execute a Bash script at `/home/user/process_archives.sh` that does the following:
1. Iterates through all `.dat` files in `/home/user/archives/` in alphabetical order.
2. Extracts and checks the 8-byte header of each file.
3. If the header is exactly `DATAv2.0`, extract the remaining gzipped payload, decompress it, and append the resulting text to a single output file: `/home/user/combined_v2.json`.
4. To ensure the script is safe for future concurrent execution, you **must** use `flock` to acquire an exclusive lock on `/home/user/combined.lock` whenever you append data to `/home/user/combined_v2.json`.
5. After processing all files, create a summary file at `/home/user/summary.txt` containing exactly two lines:
   - Line 1: The number of `DATAv2.0` files successfully processed.
   - Line 2: The total number of text lines in `/home/user/combined_v2.json`.

Run your script to produce the final `combined_v2.json` and `summary.txt` files.

Constraints:
- Use only standard bash and Linux coreutils (e.g., `dd`, `tail`, `gzip`, `flock`, etc.).
- The 8-byte header does not contain a newline character. The gzip stream starts exactly at byte 9.