You are a backup administrator recovering data from a legacy archival system. You have been provided with a custom binary archive file at `/home/user/backup.bka`. 

Recent security audits revealed that the old backup software was vulnerable to "Archive Slip" (similar to Zip Slip), meaning the archive may contain files with absolute paths or relative path traversal sequences (like `../../../etc/shadow`) that could overwrite system files if extracted naively.

Your task is to write a Go program at `/home/user/extract.go` that parses this custom binary format, safely extracts the contents to the `/home/user/safe_extract/` directory, and generates a checksum manifest.

**Archive Format (`backup.bka`):**
The archive contains a sequence of files. Each file entry is structured sequentially as follows:
1. **Filename Length**: 2 bytes, Little Endian unsigned integer (`uint16`).
2. **Filename**: Variable length UTF-8 string (length defined by the previous field).
3. **File Size**: 4 bytes, Little Endian unsigned integer (`uint32`).
4. **File Content**: Variable length byte sequence (length defined by the previous field).

*Note: The archive ends when the end of the file is reached.*

**Extraction Requirements:**
1. **Safety First:** You must strip all directory path information from the extracted filenames. Only use the base filename (e.g., `/var/log/syslog` and `../../syslog` should both be extracted safely as `syslog`).
2. **Atomic Writes:** To prevent partial file writes in case of a crash, your Go program must extract each file's content to a temporary file named `<basename>.tmp` in the `safe_extract` directory, and then atomically rename it to the final `<basename>`.
3. **Checksum Manifest:** After extracting all files, your Go program must generate a manifest file at `/home/user/manifest.txt`. This manifest should contain the SHA-256 checksums of the safely extracted files, followed by two spaces, and then the base filename. The lines in the manifest must be sorted alphabetically by the base filename.

**Output Format for `manifest.txt`:**
```
[SHA256_HEX]  [basename]
[SHA256_HEX]  [basename]
...
```

Run your Go program to perform the extraction and generate the manifest. Ensure the `/home/user/safe_extract/` directory is created before writing files to it.