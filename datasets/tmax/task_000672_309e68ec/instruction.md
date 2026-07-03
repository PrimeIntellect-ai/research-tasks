I need you to write a Rust program that acts as a secure configuration unpacker. We have a custom configuration archive format used by our deployment manager, but we recently realized it's vulnerable to "zip slip" attacks (path traversal) and writes files non-atomically. 

Your task is to write a Rust script at `/home/user/extractor.rs`, compile it to `/home/user/extractor`, and run it against the archive located at `/home/user/configs.pkg`. The extracted files should be placed inside `/home/user/extracted_configs/`.

Here is the specification for the `.pkg` binary format:
1. `[1 byte]` N: The number of files in the archive.
2. Followed by N file entries. Each entry consists of:
   - `[1 byte]` L: The length of the file path string.
   - `[L bytes]` Path: The relative file path (ASCII). Note: paths may have `.csv` extensions, which must be changed to `.json` upon extraction.
   - `[4 bytes]` P: The payload length in bytes (little-endian u32).
   - `[P bytes]` Payload: The file contents in CSV format (e.g., `key,value\n`).

Your Rust program must fulfill the following requirements:
1. **Security (Zip Slip Mitigation)**: It must detect any file entry whose path contains `../` or attempts to traverse outside the target `/home/user/extracted_configs/` directory. Any such malicious entry must be completely skipped.
2. **Format Conversion**: The payload is stored as CSV (always exactly 2 columns per line, `key,value`). Your program must convert this into a flat JSON object (e.g., `{"key":"value"}`) and write it with a `.json` extension instead of `.csv`.
3. **Atomic Writes**: To ensure the configuration manager doesn't read a partially written file, you must write the JSON payload to a temporary file (append `.tmp` to the target path) and then atomically rename it to the final target path.
4. Create any necessary parent directories for valid extracted files within `/home/user/extracted_configs/`.

Once your Rust code is ready, compile it and run it. Leave the correctly extracted JSON files in `/home/user/extracted_configs/`.