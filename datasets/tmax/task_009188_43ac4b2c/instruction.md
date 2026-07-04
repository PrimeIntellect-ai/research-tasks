You are tasked with securely managing configuration updates for a system. You have been provided with a directory of configuration update archives and a configuration manifest, but we suspect some of these archives might be malicious and vulnerable to a "Zip Slip" attack (attempting to overwrite files outside the intended extraction directory).

Your objective is to write and execute a Python script that performs the following steps:

1. Read the configuration file located at `/home/user/updates/config.json`. This file contains a JSON array of ZIP archive filenames located in the `/home/user/updates/` directory that need to be processed.
2. For each ZIP archive listed in the JSON file:
   - Verify its integrity by checking for Zip Slip vulnerabilities. An archive is considered malicious if ANY of its members have absolute paths (starting with `/`) or contain directory traversal sequences (`../` or `..\`).
   - If an archive is malicious, skip it entirely (do not extract any files from it).
   - If an archive is safe, extract its contents to `/home/user/extracted_configs/` (create this directory if it doesn't exist).
3. After processing all archives, generate a checksum manifest of the successfully extracted files.
   - Calculate the SHA256 checksum for each extracted file.
   - Write the results to `/home/user/manifest.txt`.
   - Each line in `manifest.txt` must be exactly in this format: `<sha256_hash>  <filename>` (two spaces between the hash and the base name of the file, e.g., `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  app.conf`). Sort the lines alphabetically by filename.

Ensure you process all files accurately and strictly follow the formatting requirements for `/home/user/manifest.txt`.