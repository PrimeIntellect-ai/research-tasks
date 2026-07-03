You are an AI assistant helping to build a robust indexer for an artifact manager. 

We have a repository of binary artifacts and metadata located at `/home/user/artifacts`. The structure contains versioned directories, but due to poorly managed legacy systems, there are symbolic links that create infinite loops (e.g., a `legacy` folder linking back to a parent directory).

Your task is to write and execute a Python script at `/home/user/indexer.py` that accomplishes the following:

1. **Traverse the repository**: Recursively walk through `/home/user/artifacts`.
2. **Avoid infinite loops**: You must detect and safely skip symbolic links that lead to loops or already visited directories. Whenever a symlink directory is skipped to prevent a loop, append the absolute path of that symlink to `/home/user/skipped_links.log` (one path per line).
3. **Parse and Hash**: For every `.json` file found (which contains artifact metadata like `{"name": "...", "version": "..."}`), look for a corresponding `.bin` file in the same directory with the same base name. Read the binary file and calculate its SHA256 checksum.
4. **Concurrent-Safe Manifest**: Multiple processes might eventually run this script. You must implement file locking using Python's `fcntl` module (`fcntl.flock` with `LOCK_EX`) on the output file before writing to it.
5. **Output**: Write the consolidated data to `/home/user/manifest.json`. The file must contain a single JSON array of objects. Each object must have the following exact keys:
   - `"artifact_path"`: The absolute path to the `.bin` file.
   - `"sha256"`: The calculated SHA256 checksum of the `.bin` file.
   - `"name"`: Extracted from the corresponding `.json` file.
   - `"version"`: Extracted from the corresponding `.json` file.

Run your script to ensure `/home/user/manifest.json` and `/home/user/skipped_links.log` are properly generated.