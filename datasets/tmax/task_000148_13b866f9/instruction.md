You are an AI assistant helping a technical writer who organizes documentation for a firmware engineering team.

The team receives automated documentation drops as zip archives in `/home/user/docs_incoming/`. These archives contain Markdown documentation, firmware binaries (`.elf` files), and 3D printer artifacts (`.gcode` files). 

Recently, a misconfigured build server started generating archives containing malicious "zip slip" paths (e.g., `../../home/user/overwrite_me.txt`). To safely index the metadata without risking file overwrites, you need to extract specific information *directly from the zip streams* without extracting the archives to disk.

Write a Python script at `/home/user/index_docs.py` that accepts a zip file path as a command-line argument and does the following:
1. Opens the zip file and iterates through its contents.
2. Identifies all `.elf` files. For each, reads the binary header directly from the zip stream to extract the 64-bit Entry Point address. (Assume all ELFs are 64-bit little-endian. The entry point is an 8-byte integer located at offset 0x18 in the file). Format the entry point as a hex string (e.g., `"0x400080"`).
3. Identifies all `.gcode` files. Reads the text stream to find the first line starting exactly with `; TargetMachine: ` and extracts the machine name that follows it.
4. Appends a JSON line to `/home/user/doc_index.jsonl` with the following structure:
   `{"archive": "<basename_of_zip>", "elf_entry_points": {"<filename1.elf>": "<hex_entry_point>"}, "gcode_machines": {"<filename1.gcode>": "<machine_name>"}}`
5. **Critical Requirement**: Because the build system will invoke your script concurrently on multiple archives, your script **must** use exclusive file locking (`fcntl.flock`) on `/home/user/doc_index.jsonl` while writing to prevent data corruption.

Ensure your script works correctly and run it on all zip files currently in `/home/user/docs_incoming/`.