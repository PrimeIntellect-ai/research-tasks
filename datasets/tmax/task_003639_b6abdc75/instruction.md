You are an artifact manager tasked with curating a batch of disorganized legacy binary artifacts.

An archive of binary files is located at `/home/user/artifacts.tar.gz`. The files inside currently have non-descriptive names (like `fileA.bin`). 

Your task is to write and execute a Python script to curate these artifacts by doing the following:

1. **Extract**: Extract the contents of `/home/user/artifacts.tar.gz` into a new directory `/home/user/extracted`.
2. **Parse and Validate**: Each valid binary file has a 24-byte header:
   - Bytes 0-3: Magic number. Must be exactly the ASCII string `ARTF`.
   - Bytes 4-19: True artifact name (ASCII string, null-padded `\x00` at the end).
   - Bytes 20-23: Version number (32-bit unsigned integer, little-endian).
   If a file does not have the magic number `ARTF`, it is corrupt. Delete it.
3. **Bulk Rename**: Rename the valid files in the `/home/user/extracted` directory to follow the pattern `<true_name>_v<version>.bin` (e.g., if the true name is `libnet` and version is `3`, rename the file to `libnet_v3.bin`). Strip any null padding from the extracted true name.
4. **Atomic Registry Generation**: Create a JSON file at `/home/user/registry.json` that maps the *new* file names to their *original* extracted file names. For example: `{"libnet_v3.bin": "fileA.bin"}`. 
   *Enterprise Constraint*: To ensure the registry is never read in a partially written state, you must write the JSON data to a temporary file first, and then perform an atomic rename to `/home/user/registry.json` using Python's `os.replace`.
5. **Archive**: Create a new ZIP archive at `/home/user/curated.zip` containing ONLY the renamed `.bin` files (do not include any parent directories in the zip file structure).

Ensure your script handles the binary parsing correctly and produces the exact output paths requested.