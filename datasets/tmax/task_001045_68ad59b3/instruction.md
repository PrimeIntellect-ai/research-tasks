You are an AI assistant helping a developer securely ingest and organize a set of project files provided by an external vendor.

The vendor has provided a large archive that they split into multiple chunks to bypass email size limits. We suspect their archiving tool was faulty or compromised, as there are reports that extracting their archives can overwrite files outside the intended destination directory (a vulnerability known as "Zip Slip").

Your task is to safely reconstruct, extract, organize, and catalog this data using Python.

Here are your instructions:
1. **Reconstruct the Archive:**
   In `/home/user/incoming/`, you will find several chunked files named `vendor_data.tar.gz.part1`, `vendor_data.tar.gz.part2`, etc. Merge these chunks in numerical order to reconstruct the compressed tar archive.

2. **Safe Extraction (Prevent Zip Slip):**
   Extract the contents of the archive into `/home/user/workspace/extracted/`.
   **CRITICAL:** You must write a Python script to perform the extraction safely. Do not use the standard `tar` command line tool directly unless you can guarantee it strictly filters paths. Skip any file entry in the archive that attempts to write outside of the target extraction directory (e.g., entries containing `../` that resolve outside the root, or absolute paths like `/tmp/...` or `/home/...`). Only extract safe files.

3. **Deduplication via Symbolic Links:**
   The vendor often includes duplicate files, which wastes space. After extracting the safe files, scan the `/home/user/workspace/extracted/` directory for identical files (based on their content).
   For any set of identical files, keep the file that comes first alphabetically by its relative path. Replace all other identical files with a **symbolic link** pointing to the kept file. The symbolic links must use relative paths to resolve correctly even if the whole directory is moved.

4. **Generate a Manifest:**
   Generate a JSON manifest file at `/home/user/workspace/manifest.json` that catalogs the final state of the `extracted` directory.
   The JSON should be an object where the keys are the relative file paths (e.g., `dir1/file.txt`) from the `extracted/` directory, and the values are objects with the following keys:
   - `"type"`: `"file"` or `"symlink"`
   - `"sha256"`: The SHA-256 checksum of the file content (if it's a file), or `null` if it's a symlink.
   - `"target"`: The relative path to the target file if it's a symlink, or `null` if it's a regular file.

Ensure your Python script handles the binary formats, compressed streams, and link management robustly.