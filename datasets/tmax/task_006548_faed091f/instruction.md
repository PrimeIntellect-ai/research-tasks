You are an AI assistant helping a technical writer organize their documentation. The writer has a large directory of documentation files, but they accidentally created some symbolic link loops while trying to link different modules together. They need a Python script to index recently modified files without getting trapped in an infinite loop.

Write and execute a Python script at `/home/user/index_docs.py` that does the following:

1. Recursively traverses the directory `/home/user/docs_root`, following symbolic links.
2. Safely handles symlink loops by keeping track of visited real paths (avoiding infinite recursion).
3. Identifies all `.md` and `.txt` files that have a modification time (mtime) strictly greater than or equal to `1704067200` (which is 2024-01-01 00:00:00 UTC).
4. For each qualifying file, reads the first non-empty line (stripping leading/trailing whitespace).
5. Creates a dictionary mapping the absolute real path of the file to its first non-empty line.
6. Writes this dictionary as a formatted JSON file (with 4 spaces indentation) to `/home/user/recent_index.json`. 
7. To prevent data corruption, the JSON file must be written atomically (write to a temporary file in `/home/user` first, then replace the target file).
8. After creating the JSON file, create a gzip-compressed version of it at `/home/user/recent_index.json.gz`.

Run your script so that `/home/user/recent_index.json` and `/home/user/recent_index.json.gz` are generated successfully.