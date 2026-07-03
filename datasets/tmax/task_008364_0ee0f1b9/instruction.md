You are a developer tasked with organizing and verifying incoming build artifacts for a large project. The artifacts are stored as compressed tar archives, but there has been a security warning: some of the archives might be intentionally crafted to overwrite system files when extracted by exploiting directory traversal vulnerabilities (similar to "Zip Slip" attacks). 

Your task is to write a Bash script at `/home/user/process_builds.sh` that safely filters, extracts, and analyzes these artifacts.

You must implement the following logic in your script:
1. Process all `.tar.gz` archives located in `/home/user/incoming/`.
2. Inspect the contents of each archive before extraction. If an archive contains any member path that starts with `/` (absolute path) or contains `../` (parent directory traversal), you must consider the entire archive compromised.
3. For compromised archives: DO NOT extract them. Append the base name of the archive (e.g., `malicious.tar.gz`) to `/home/user/quarantine.log`.
4. For safe archives: Extract their contents into `/home/user/extracted/`.
5. After all safe archives are extracted, scan the `/home/user/extracted/` directory for all valid ELF binaries.
6. For every ELF binary found, generate a SHA256 checksum and parse its Entry Point Address (e.g., `0x401000`).
7. Write these details to a manifest file at `/home/user/elf_manifest.txt`. Each line should be formatted exactly as: `<sha256sum> <basename> <entry_point>`
8. The lines in `/home/user/elf_manifest.txt` must be sorted alphabetically by the `<basename>` of the ELF file.

Constraints & Notes:
- Create the `/home/user/extracted/` directory if it does not exist.
- Use native Linux tools (like `tar`, `readelf`, `sha256sum`, `file`).
- Do not install any external Python libraries or non-standard tools.
- Your final deliverable is the execution of your script, which results in the correct population of `/home/user/extracted/`, `/home/user/quarantine.log`, and `/home/user/elf_manifest.txt`.