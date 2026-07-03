You are a backup administrator tasked with archiving recovered data from a compromised server. The data is located in `/home/user/recovery`. You need to process this data, redact sensitive information, extract binary signatures, and package it into a clean archive.

Perform the following steps using bash and standard Linux command-line tools:

1. **Metadata Search & Binary Extraction**:
   - Find all `.dat` files in `/home/user/recovery/data/` that are strictly larger than 10 Kilobytes (10240 bytes).
   - For each of these files, extract the first 4 bytes (the file signature/magic number) and convert it to a lowercase hexadecimal string.
   - Create a manifest file at `/home/user/archive_manifest.txt`. Each line should be in the format `filename.dat: hex_string` (e.g., `backup.dat: 89504e47`).
   - Sort the lines in the manifest file alphabetically by filename.

2. **Large-scale Text Editing**:
   - There are log files in `/home/user/recovery/logs/`.
   - Create a new directory `/home/user/clean_logs/`.
   - Copy all `.log` files from `/home/user/recovery/logs/` to `/home/user/clean_logs/`, but during the process, redact all IPv4 addresses. 
   - Replace every valid-looking IPv4 address (e.g., `192.168.1.100`, `10.5.2.1`) with the exact string `XXX.XXX.XXX.XXX`.

3. **Archiving**:
   - Create a compressed tarball at `/home/user/safe_backup.tar.gz`.
   - The archive must contain exactly two items at its root: 
     a) The `archive_manifest.txt` file
     b) The `clean_logs` directory (and its redacted log files).
   - Do NOT include the original `/home/user/recovery` directory or the unredacted logs in the archive.

Ensure all paths and file contents strictly match these requirements.