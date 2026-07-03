You are acting as a backup administrator. You have received a legacy text-based archive file at `/home/user/backup_archive.txt` from an old remote server. This archive uses a custom format to pack multiple log files together. 

Unfortunately, the system that generated this archive was known to be vulnerable to path traversal (similar to "zip slip"), and some file paths in the archive might contain dangerous relative paths (e.g., `../../../home/user/.bashrc`). Furthermore, the text files were encoded using different character sets depending on the source machine.

Your task is to write a Bash script (e.g., `/home/user/extract.sh`) and execute it to securely parse and extract this archive into the `/home/user/extracted_logs/` directory.

### Requirements

1. **Path Sanitization**:
   For each file in the archive, extract **only the basename** of the provided file path. Discard any directory components to prevent path traversal. All extracted files must be placed directly inside `/home/user/extracted_logs/`.

2. **Encoding Conversion**:
   Read the specified encoding for each file. When extracting the data block, you must convert the content from its original encoding to `UTF-8` (using `iconv`) before saving it.

3. **Atomic Writes and Temp Files**:
   To prevent incomplete files from being read by a concurrently running log processor, you must extract each file atomically. 
   - First, write the converted `UTF-8` content to a temporary file in `/home/user/extracted_logs/` (e.g., using a `.tmp` suffix).
   - Once the write is completely finished, rename (`mv`) it to its final filename (the basename extracted above).

4. **Concurrent Audit Logging**:
   Every time a file is successfully extracted and moved to its final location, you must append a record to an audit log located at `/home/user/extraction_audit.log`. 
   - The log entry format must be: `EXTRACTED: <basename>`
   - Because other administrative tools might write to this audit log at the same time, you **must** use `flock` to acquire an exclusive lock on the audit log before appending to it.

### Archive Format (`/home/user/backup_archive.txt`)

The archive consists of multiple file entries formatted exactly like this:
```
[BEGIN_FILE]
Path: <file_path>
Encoding: <encoding>
[DATA]
<file content... can be multiple lines>
[END_FILE]
```

### Constraints
- Do not use Python, Perl, or other scripting languages. The solution must be implemented using Bash and standard CLI utilities (`grep`, `sed`, `awk`, `iconv`, `flock`, `mv`, etc.).
- Ensure `/home/user/extracted_logs/` is created if it does not exist.