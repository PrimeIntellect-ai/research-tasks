You are tasked with helping organize and audit a set of legacy project files. I have an archive containing several nested compressed backups and a configuration file. Some of these nested backups might be corrupted due to age, and I need to extract specific binary signatures from the valid ones based on a manifest.

Here is the current state of the system:
- A directory exists at `/home/user/workspace/`
- Inside this directory, there is an uncompressed tarball named `/home/user/workspace/legacy_project.tar`.

The `legacy_project.tar` contains:
1. A JSON configuration file named `manifest.json`. This file contains a dictionary mapping the names of inner zip archives to specific target filenames located inside those zips (e.g., `{"backup1.zip": "asset_A.bin", ...}`).
2. Several zip files (e.g., `backup1.zip`, `backup2.zip`, etc.).

Your task is to write a script (in Python, Bash, or any combination of tools) to perform the following operations:
1. Extract `/home/user/workspace/legacy_project.tar`.
2. Parse `manifest.json` to find the mapping of zip archives to their target files.
3. For each zip archive listed in the manifest, verify its archive integrity. If the zip file is corrupted or invalid, you must skip it entirely and proceed to the next one.
4. If the zip archive is valid, extract the specific target file named in the manifest from that zip.
5. Read the first 4 bytes (the "magic number" or file header) of the extracted target file.
6. Format these 4 bytes as a contiguous, lowercase hexadecimal string (exactly 8 hex characters, e.g., `89504e47`).
7. Append this result to a log file located at `/home/user/workspace/headers.log`.

The output in `/home/user/workspace/headers.log` must contain exactly one line per *valid* archive in the exact following format:
`<zip_filename>:<target_filename>:<4-byte_hex_header>`

For example, if `backup1.zip` is valid, contains `asset_A.bin`, and its first 4 bytes are `\x7fELF`, the line should read:
`backup1.zip:asset_A.bin:7f454c46`

Order does not matter in the final log file, but you must only include entries for archives that successfully pass integrity checks and contain the specified target files.