You are tasked with developing a secure artifact ingestion tool in Rust for our binary repository manager. We receive artifact bundles in a custom binary format, but we've detected that some uploaded bundles attempt to perform directory traversal attacks (similar to "Zip Slip") by including paths that resolve outside the intended extraction directory.

Your objective is to create a Rust CLI tool that extracts these bundles safely, parses contained ELF binaries, converts character encodings of metadata, and produces a final report.

### Task Requirements

1. **Create a Rust Project:**
   Create a new Rust binary project at `/home/user/artifact_manager`. You may use third-party crates like `goblin` (for ELF parsing) and `byteorder`.

2. **Process the Custom Archive:**
   The tool must read a custom binary archive located at `/home/user/artifacts/bundle.bin`.
   The binary format is specified as follows:
   - **Magic Header:** 4 bytes ASCII `ARTF`
   - **File Count:** 1 unsigned 32-bit integer (Little Endian)
   - **File Entries** (repeated *File Count* times):
     - **Path Length (N):** 1 unsigned 16-bit integer (Little Endian)
     - **Path:** N bytes (UTF-8 string)
     - **File Size (S):** 1 unsigned 32-bit integer (Little Endian)
     - **File Data:** S bytes of raw file content

3. **Secure Extraction (Zip Slip Prevention):**
   Extract the files into `/home/user/extracted/`.
   - **Security Rule:** If a file's path attempts to escape the extraction directory (e.g., contains `../` resolving out of bounds, or is an absolute path), you **must not** extract it.
   - For every malicious path detected, append a line exactly matching `MALICIOUS: <original_path>` to `/home/user/extraction.log`.

4. **ELF Parsing:**
   For any successfully extracted file ending in `.elf`, parse the ELF header to find its entry point address (as a hexadecimal string formatted like `0x401000`).

5. **Encoding Conversion:**
   The archive contains a file named `metadata.txt` which is encoded in UTF-16LE. Convert its contents to UTF-8.

6. **Final Report:**
   Write a final report to `/home/user/report.json` in the following exact JSON format:
   ```json
   {
     "extracted_files": ["list", "of", "safely", "extracted", "paths"],
     "malicious_files_prevented": 1,
     "elf_entry_points": {
       "path/to/file.elf": "0x..."
     },
     "metadata_text": "<the UTF-8 decoded contents of metadata.txt>"
   }
   ```
   *Note: The `extracted_files` list should contain the relative paths as specified in the archive, not the absolute paths on disk.*

Run your tool to process `/home/user/artifacts/bundle.bin` and generate the required outputs.