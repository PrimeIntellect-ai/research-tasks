You are an AI assistant helping a technical writer organize a large influx of documentation updates. 

The writer has received a compressed archive of markdown documentation from various contributors at `/home/user/raw_docs.tar.gz`. You need to process this archive, split large files for the new pagination system, and generate a concurrently-safe manifest.

Please write a Python script at `/home/user/process_docs.py` that performs the following tasks:

1. **Archive Verification & Stream Processing:**
   - The script must accept a tar.gz archive path as a command-line argument.
   - It should first verify the integrity of the gzip file. If the archive is corrupted, the script must exit with status code 1.
   - It must read the files directly from the compressed archive stream (without extracting the entire archive to disk beforehand).

2. **File Chunking:**
   - Extract only `.md` files.
   - Any markdown file strictly greater than 50 lines must be split into chunks of exactly 50 lines (the final chunk may have fewer).
   - Save the processed files to the directory `/home/user/processed_docs/` (create it if it doesn't exist).
   - If a file is 50 lines or less, save it as `<filename>.md`.
   - If a file is split, save the chunks as `<filename>_part<N>.md` where `N` starts at 1. (e.g., `guide_part1.md`, `guide_part2.md`).

3. **Concurrent Processing & File Locking:**
   - To speed up processing for massive archives, process the files extracted from the stream concurrently using Python's `multiprocessing` module.
   - Every time a file (or its chunks) is successfully written to `/home/user/processed_docs/`, the worker process must append a JSON record to a manifest file at `/home/user/manifest.jsonl`.
   - The JSON record must be exactly in this format (one JSON object per line): `{"original": "filename.md", "chunks": ["filename_part1.md", "filename_part2.md"]}` (or `{"original": "intro.md", "chunks": ["intro.md"]}` for unsplit files).
   - Because multiple processes will write to `manifest.jsonl` simultaneously, you **must** use `fcntl.flock` (exclusive lock) to prevent race conditions during the append operation.

After writing the script, execute it on `/home/user/raw_docs.tar.gz`. 

Finally, generate a SHA256 checksum of the resulting `/home/user/manifest.jsonl` and save the hash to `/home/user/manifest_checksum.txt` (just the hash and the filename, as output by the `sha256sum` command).

Ensure your script handles all the above constraints correctly.