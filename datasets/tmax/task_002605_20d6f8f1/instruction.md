You are an artifact manager tasked with curating a legacy binary repository. You need to clean up corrupted metadata, compute cryptographic hashes of binary blobs, and reorganize the repository into a modern, hash-addressed structure.

You have been given a legacy directory at `/home/user/legacy_repo`. Inside, there are several binary files (`.blob`) and a corrupted metadata file named `metadata.csv`.

Here are your instructions:

1. **Text Transformation (Shell):** 
   The `/home/user/legacy_repo/metadata.csv` file is messy. It uses pipes (`|`) instead of commas, has Windows-style line endings (CRLF), and some of the `name` fields are polluted with HTML bold tags (`<b>` and `</b>`). 
   Using command-line text transformation tools (like `sed`, `awk`, `tr`, etc.), clean this file and output it to `/home/user/clean_metadata.csv`. The clean file must:
   - Use standard commas (`,`) as delimiters.
   - Use Unix-style line endings (LF).
   - Have no `<b>` or `</b>` tags.
   - Keep the original header: `id,name,version,blob_file`

2. **Binary Processing and Organization (Python):**
   Write and execute a Python script `/home/user/curate.py` that reads `/home/user/clean_metadata.csv`. For each row:
   - Read the corresponding binary file from `/home/user/legacy_repo/<blob_file>`.
   - Compute the SHA-384 hash of the binary file's contents.
   - Copy the binary file to a new curated directory structure: `/home/user/curated_repo/<prefix>/<hash>.blob`, where `<prefix>` is the first 2 characters of the SHA-384 hash, and `<hash>` is the full SHA-384 hex digest.

3. **Structured Format Output (Python):**
   Your Python script must also generate a registry file at `/home/user/curated_repo/registry.json`. This must be a single JSON array containing objects for every successfully processed artifact. Each object must have exactly these keys:
   - `id`: (string) The artifact ID from the CSV.
   - `name`: (string) The cleaned artifact name.
   - `version`: (string) The version from the CSV.
   - `sha384`: (string) The computed SHA-384 hex digest.
   - `curated_path`: (string) The absolute path to the new blob file (e.g., `/home/user/curated_repo/a1/a1b2...blob`).

4. **Pipeline Query:**
   Finally, find all `.blob` files in `/home/user/curated_repo/` that are strictly larger than 500 bytes. Pipe their absolute paths into `/home/user/large_blobs.txt`, one path per line, sorted alphabetically.

Ensure all directories are created as needed and permissions allow reading and writing by the `user` account.