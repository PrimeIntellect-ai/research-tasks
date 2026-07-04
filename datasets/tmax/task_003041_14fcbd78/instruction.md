I am a developer organizing my project files, and I've recovered an old backup archive from a simulated mounted drive. The archive uses a proprietary, custom text-based format and I need you to extract it, but only if the files within it pass their integrity checks.

The archive is located somewhere under the directory `/home/user/projects/archive_mount/`. You need to find a file named `backup.arc`.

**Archive Format Specification:**
The `backup.arc` file contains multiple archived files. Each file entry is structured exactly as follows (each delimiter is on its own line):
1. `===FILENAME: <filename>===`
2. `===CHECKSUM: <md5_hex_digest>===`
3. The file content, which has been hex-encoded (a single continuous string of hexadecimal characters).
4. `===END_FILE===`

**Your Task:**
1. Find `backup.arc`.
2. Write a Python script to parse the archive.
3. For each file entry in the archive, decode the hex content back to its original bytes.
4. Calculate the MD5 hash of the *decoded* bytes.
5. Compare your calculated MD5 hash against the hash provided in the `===CHECKSUM: <md5_hex_digest>===` line.
6. If the checksum matches (integrity verified), save the decoded bytes to a file named `<filename>` inside the directory `/home/user/projects/restored/`. 
7. If the checksum does NOT match, skip the file entirely (do not extract it) and log its name to `/home/user/projects/restored/corrupted.log` (one filename per line).

You must create the `/home/user/projects/restored/` directory before extracting. Use Python to handle the parsing, hex-decoding, and MD5 verification.