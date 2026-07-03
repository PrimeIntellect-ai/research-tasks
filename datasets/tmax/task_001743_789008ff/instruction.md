You are tasked with recovering our configuration management system after a severe log rotation race condition corrupted several configuration state archives. We need to implement a robust filter that can analyze nested configuration backups and reject any that contain corrupted or maliciously injected Write-Ahead Log (WAL) entries.

You must create a validation script at `/home/user/filter.sh`. 

**The Input:**
Your script will be invoked with a single argument: the path to a primary backup archive (`.tar` format).
Inside this primary archive are multiple nested `.tar.gz` files, and inside *those* are the actual `.wal` (Write-Ahead Log) configuration tracking files.

**The WAL Format:**
Each `.wal` file contains configuration changes recorded in the following plain-text format, one entry per line:
`[TIMESTAMP] ACTION | KEY | VALUE | CHECKSUM`

**Validation Rules:**
To determine if a top-level `.tar` archive is "CLEAN" or "EVIL" (corrupted/malicious), your script must recursively extract all nested archives and validate every single `.wal` file. 

The validation logic (allowed actions, and the salt used to generate the checksum) was documented in an architecture diagram recently saved to the server at `/app/architecture_diagram.png`. You will need to inspect this image to extract the exact `SALT` string and the list of permitted `ACTIONS`. 

A `.wal` entry is valid IF AND ONLY IF:
1. The `ACTION` is one of the permitted actions listed in the architecture diagram.
2. The `CHECKSUM` exactly matches the standard MD5 hex digest of the string formed by concatenating: `ACTION` + `KEY` + `SALT` (in that exact order, with no spaces in between).

An archive is considered **EVIL** if *any* `.wal` file inside it contains *any* invalid entry. Otherwise, it is **CLEAN**.

**Your Script's Output:**
- If the archive is CLEAN, your script must exit with status code `0`.
- If the archive is EVIL, your script must exit with a non-zero status code (e.g., `1`).
- You may use standard Unix tools (bash, tar, gzip, md5sum, grep, awk, python, tesseract, etc.). Ensure your script handles temporary extraction directories cleanly.

Please write `/home/user/filter.sh`. Once you are done, you do not need to run tests manually—our automated verification suite will test your script against a corpus of known clean and evil archives.