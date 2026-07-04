You are helping a researcher organize and archive a deeply nested dataset. Due to a faulty automated pipeline, the dataset directory contains symlinks that point back to higher-level directories, creating infinite loops. 

Your task is to write and execute a Python script (`/home/user/archive_data.py`) that safely reads the dataset, splits large files into manageable chunks, and generates a verified manifest.

Here are the requirements for your script:

1. **Configuration Interpretation:**
   Read the configuration file located at `/home/user/dataset/config.ini`. It uses the standard INI format and contains an `[Archive]` section with the following keys:
   - `chunk_size_bytes`: Integer representing the maximum size of each split chunk.
   - `target_extension`: The file extension to process (e.g., `.dat`).
   - `output_dir`: The absolute path where the chunks and manifest should be saved.

2. **Safe Traversal & Chunking:**
   - Traverse the directory `/home/user/dataset/` to find all files matching the `target_extension`.
   - **Important:** You must *follow* symlinks to discover files in linked directories, but you must implement cycle detection to avoid infinite loops caused by recursive symlinks.
   - For every matching file found, read it and split it into chunks of exactly `chunk_size_bytes` (the last chunk may be smaller).
   - Save the chunks in the `output_dir`. The output filename must be constructed by taking the file's path *relative to `/home/user/dataset/`*, replacing all directory separators (`/`) with underscores (`_`), and appending `_part<N>.chunk`, where `<N>` is the 0-indexed part number.
     *Example:* `/home/user/dataset/nested/file.dat` split into two chunks would produce `nested_file.dat_part0.chunk` and `nested_file.dat_part1.chunk`.

3. **Manifest and Checksum Generation:**
   - Calculate the SHA-256 checksum for each generated chunk.
   - Output these checksums to a manifest file at `<output_dir>/manifest.txt`.
   - Each line in the manifest must be exactly in this format: `<sha256_hex_hash>  <chunk_filename>` (using two spaces between the hash and the filename).
   - The lines in the manifest must be sorted alphabetically by the `<chunk_filename>`.

Write the Python script, run it, and ensure that the final `/home/user/archive_output/manifest.txt` is generated exactly as specified.