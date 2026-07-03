You are a storage administrator responding to an incident. A poorly written extraction script recently unpacked a user-provided archive into `/home/user/storage_pool/`. Due to a path traversal vulnerability (similar to "zip slip"), some files escaped the intended directory and overwrote files in a sensitive directory. Additionally, the intended directory is bloated with duplicate files.

Your job is to clean up the storage pool, fix encodings, deduplicate files to save disk space, and standardize filenames using bash and standard Linux CLI utilities. 

Here are the details of the environment and your objectives:

**Directory Structure:**
- `/home/user/storage_pool/logs/extract.log`: A multi-line log file detailing the extraction process.
- `/home/user/storage_pool/critical/`: A directory containing sensitive system configuration files.
- `/home/user/storage_pool/intended/`: The directory where the archive was *supposed* to be extracted.

**Log Format (`extract.log`):**
The log consists of multi-line records formatted exactly like this:
```
---
Time: 2023-10-25 14:00:01
Extracted-To: ../critical/escaped_file_1.conf
Bytes: 1024
Status: SUCCESS
---
```
*(Note: Paths in `Extracted-To` are relative to `/home/user/storage_pool/intended/`, meaning `../critical/` resolves to `/home/user/storage_pool/critical/`)*

**Phase 1: Incident Response (Log Parsing & Encoding Conversion)**
1. Parse `/home/user/storage_pool/logs/extract.log` to identify all files that successfully extracted to the `../critical/` directory.
2. The extracted files in the `critical/` directory were written in `UTF-16LE` encoding, which is breaking our systems. For *only* the files identified in the log as successfully extracted to `../critical/`, convert their character encoding to `UTF-8` in-place (meaning the final file must have the exact same name and path but be UTF-8 encoded).

**Phase 2: Space Management (Deduplication via Hard Links)**
1. The `/home/user/storage_pool/intended/` directory contains many identical large files. To save disk space, find all duplicate files within this directory.
2. For each set of identical files, keep the file that comes first alphabetically by its full filename. Replace all other identical files in that set with a **hard link** to the alphabetically first file. 

**Phase 3: Bulk Renaming**
1. Standardize the naming in `/home/user/storage_pool/intended/`. Find all files in this directory ending in `.dat`.
2. Replace any spaces in their filenames with underscores (`_`).
3. Change their extension from `.dat` to `.bak`.
*(e.g., "report 2023.dat" becomes "report_2023.bak")*

Complete all three phases. Use standard bash shell commands (`awk`, `sed`, `find`, `iconv`, `ln`, `mv`, etc.) or scripts to accomplish these tasks. Do not delete the log file.