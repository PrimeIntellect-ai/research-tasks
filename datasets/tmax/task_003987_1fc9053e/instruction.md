You are tasked with writing a Python script to act as a security scanner for a configuration manager. The configuration manager processes custom binary configuration bundles (with the extension `.cfgpack`), but we suspect malicious actors might try to exploit an archive extraction vulnerability (similar to "Zip Slip") by including absolute paths or directory traversals in the archive.

Write a script at `/home/user/scan_configs.py` that does the following:

1. **Metadata-based File Search:**
   Find all `.cfgpack` files within `/home/user/incoming/` (and its subdirectories) that have been modified within the last 24 hours. Ignore older files.

2. **Binary Format Extraction:**
   For each matched file, parse the custom binary format to inspect the target paths of the files inside it. You do not need to extract the files, only parse the headers.
   
   The `.cfgpack` format specification:
   - **Magic Header:** The first 4 bytes are always the ASCII string `CFGP`.
   - **Number of Entries:** The next 2 bytes represent the number of files in the bundle (unsigned 16-bit integer, little-endian).
   - **Entries:** For each file, the structure is:
     - **Path Length:** 2 bytes (unsigned 16-bit integer, little-endian).
     - **Path:** A UTF-8 string of length equal to the Path Length.
     - **Data Length:** 4 bytes (unsigned 32-bit integer, little-endian).
     - **Data:** Raw bytes of length equal to the Data Length.

3. **Malicious Path Detection:**
   A `.cfgpack` is considered **malicious** if *any* of its parsed paths:
   - Start with `/` or `\`
   - Contain `../` or `..\` 

   If all paths are safe (e.g., `config/settings.ini`), the file is considered **safe**.

4. **Atomic Write Reporting:**
   The script must output a JSON report to `/home/user/scan_report.json`. To prevent other processes from reading an incomplete file, you **must** write to a temporary file in `/home/user/` first and then atomically move/replace it to `/home/user/scan_report.json`.
   
   The JSON format must be exactly:
   ```json
   {
     "safe_packs": [
       "/home/user/incoming/path/to/safe1.cfgpack"
     ],
     "malicious_packs": [
       "/home/user/incoming/path/to/evil1.cfgpack"
     ]
   }
   ```
   *Note: The lists of paths must be absolute paths and sorted alphabetically.*

Once you have written the script, execute it to generate the report.