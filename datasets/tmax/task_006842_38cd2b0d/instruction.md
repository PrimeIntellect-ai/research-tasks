You are acting as a backup administrator recovering data from an old, fragmented system. You have been given a set of split archive files and a corrupted XML manifest. Furthermore, these archives are known to occasionally contain dangerous paths (Zip Slip vulnerabilities) that could overwrite critical system files if extracted naively.

Your objective is to fix the manifest, assemble the archive, and safely extract it using Python.

Follow these steps exactly:

1. **Fix the Manifest**: 
   In `/home/user/manifest.xml.broken`, the XML tags for the archive parts are corrupted. The opening tags look like `[part id="1"]` instead of `<part id="1">`, and the closing tags look like `</prt>` instead of `</part>`. 
   Use standard bash text-editing tools (like `sed` or `awk`) to fix these errors and redirect the output to a valid XML file at `/home/user/manifest.xml`.

2. **Assemble the Archive**:
   Read `/home/user/manifest.xml` to determine the correct order of the chunk files (which are located in `/home/user/parts/`). Merge them in the exact order specified by the `id` attributes to create the complete archive at `/home/user/complete_backup.tar.gz`.

3. **Safe Extraction**:
   Write a Python script at `/home/user/safe_extract.py` that processes `/home/user/complete_backup.tar.gz`.
   The script must:
   - Iterate through the members of the tar file.
   - Determine if a member is "safe" or "dangerous". A path is dangerous if it is an absolute path (starts with `/`) or if it attempts to escape the extraction directory (contains `../` or resolves to a location outside the target directory).
   - Extract ONLY the safe files into `/home/user/safe_restore/` (creating the directory if it doesn't exist).
   - Write the exact original path names of all detected *dangerous* files into a JSON array, saving it to `/home/user/quarantine.json`.

After completing all operations, you should have the repaired manifest, the assembled tarball, the safely extracted logs, and the quarantine JSON file.