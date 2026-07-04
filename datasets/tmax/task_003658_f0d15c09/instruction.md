You are acting as a storage administrator. A legacy backup script went rogue and filled `/home/user/backups/raw/` with a mess of poorly named files, deeply nested archives, and infinite symlink loops. 

Your task is to write a Python script at `/home/user/cleanup.py` and run it to untangle this mess and recover the underlying data.

Here are the specific requirements for your script:
1. **Handle Symlinks:** The `raw/` directory contains symlinks. Some of them point to each other in an infinite loop. Your script must safely detect and skip any infinite symlink loops.
2. **Identify Archives by Binary Header:** The file extensions in the directory are completely mangled (e.g., `.dat`, `.tmp`). You must identify actual archive files by reading their binary magic numbers (headers). 
   - Identify ZIP files (starts with `50 4B 03 04`).
   - Identify GZIP files (starts with `1F 8B`).
3. **Extract Nested Archives:** Extract any identified ZIP or GZIP files into a temporary processing space. If an extracted file is *also* an archive (ZIP or GZIP), extract that as well. Support up to 3 levels of archive nesting.
4. **Isolate and Rename Data:** Any *non-archive* files (either sitting directly in `raw/` or extracted from the archives) must be placed in `/home/user/backups/clean/`. As you move them, bulk rename them by prepending `recovered_` to their base filename.
5. **Generate a Manifest:** After extracting and renaming the files, generate a JSON manifest at `/home/user/backups/manifest.json`. The JSON should be a single dictionary where the keys are the final filenames (e.g., `recovered_data.txt`) and the values are the SHA256 checksums (in hex) of those files.

Ensure the final manifest ONLY contains the final recovered, non-archive data files. Do not include the original mangled archives or symlinks in the `clean/` directory or the manifest.