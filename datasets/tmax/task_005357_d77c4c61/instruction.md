As a technical writer organizing our new documentation system, I received a custom documentation bundle (`/home/user/docs_archive.docpack`) from a third-party contractor. I need you to write a Python script at `/home/user/extract_docs.py` to safely parse and extract this binary file.

The `.docpack` file is a custom binary format. Its structure is:
1.  **Magic Bytes**: 4 bytes, ascii string `DOCP`.
2.  **File Count**: 4 bytes, unsigned 32-bit integer, little-endian.
3.  **File Entries** (repeated *File Count* times):
    *   **Path Length**: 2 bytes, unsigned 16-bit integer, little-endian.
    *   **Path String**: Variable length (specified by Path Length), UTF-8 encoded string representing the file path.
    *   **File Size**: 4 bytes, unsigned 32-bit integer, little-endian.
    *   **File Content**: Variable length (specified by File Size), raw binary or text data.

**Requirements:**
1.  **Configuration**: Read `/home/user/doc_config.ini`. It has a `[Settings]` section with an `output_dir` key. Create this directory if it doesn't exist and extract all files into it.
2.  **Security (Zip-Slip Mitigation)**: The contractor's packing tool had a bug, and some paths in the archive contain malicious or erroneous directory traversal sequences (like `../../../`). To prevent files from being written outside the target `output_dir`, **you must flatten all paths**. Extract every file using *only its base filename* (e.g., `some/dir/../../file.txt` should simply be saved as `file.txt` inside the `output_dir`).
3.  **Extraction**: Parse the binary headers and write the content of each file to the flattened path in the `output_dir`.
4.  **Manifest & Checksums**: After extracting all files, generate a JSON manifest file at `/home/user/manifest.json`. It should be a single dictionary mapping the extracted base filenames to their SHA-256 hexadecimal checksums.
    Format:
    ```json
    {
      "file1.txt": "a3b...c",
      "file2.png": "d4e...f"
    }
    ```

Run your Python script to complete the extraction and generate the manifest.